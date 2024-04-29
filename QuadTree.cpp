#include "QuadTree.h"

#define all(c) c.begin(), c.end()
#define dist(x1, y1, x2, y2) (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

QuadTreeNode::QuadTreeNode(vector<float> _boundary, int _level) {
    box = _boundary;
    level = _level;
}

bool QuadTreeNode::isLeaf() {
    if (children[NW] == NULL)
        return true;
    return false;
}

void QuadTreeNode::packing(Input &R) {
    for (auto r : R)
        data.push_back(r);
    packing();
}

void QuadTreeNode::packing() {
    if (data.size() > CAPACITY) {
        if (isLeaf())
            divide();
        for (auto r : data) {
            for (auto c : children) {
                if (c->intersects(r)) {
                    c->data.push_back(r);
                    break;
                }
            }
        }
        data.clear();
        for (auto c : children)
            c->packing();
    }
}

QuadTreeNode *QuadTreeNode::insert(Record r) // return leaf that is inserted, nullptr if not in range
{
    if (isLeaf()) {
        if (!this->intersects(r)) return nullptr;
        data.push_back(r);
        if (data.size() > CAPACITY) {
            divide();
            QuadTreeNode *ret_leaf = this;
            for (auto rec : data) {
                auto c = children.begin();
                while (!(*c)->intersects(rec))
                    c++;
                (*c)->data.push_back(rec);
                if (&rec == &r) // found r
                    ret_leaf = *c;
            }
            data.clear();
            return ret_leaf;
        } else {
            return this;
        }
    } else {
        auto c = children.begin();
        while (!(*c)->intersects(r)) {
            c++;
            if (c == children.end()) return nullptr;
        }
        return (*c)->insert(r);
    }
}

QuadTreeNode *QuadTreeNode::insert(Record r, queue<QuadTreeNode *> &parentQueue, int maxQueueSize = 1) // return leaf that is inserted, nullptr if not in range
{
    if (parentQueue.size() >= maxQueueSize) {
        parentQueue.pop();
    }
    if (isLeaf())
    {
        if (!this->intersects(r))
            return nullptr;
        data.push_back(r);
        if (data.size() > CAPACITY)
        {
            divide();
            QuadTreeNode *ret_leaf = this;
            for (auto rec : data)
            {
                auto c = children.begin();
                while (!(*c)->intersects(rec))
                    c++;
                (*c)->data.push_back(rec);
                if (&rec == &r) // found r
                    ret_leaf = *c;
            }
            data.clear();
            parentQueue.emplace(ret_leaf);
            return ret_leaf;
        }
        else
        {
            parentQueue.emplace(this);
            return this;
        }
    }
    else
    {
        parentQueue.emplace(this);
        auto c = children.begin();
        while (!(*c)->intersects(r))
        {
            c++;
            if (c == children.end())
                return nullptr;
        }
        return (*c)->insert(r, parentQueue);
    }
}

void QuadTreeNode::divide() {

    float xMid, yMid;
    if (POINT_SPLIT) {
        data.sortData();
        auto median = data[data.size() / 2];
        xMid = median.box[XLOW];
        yMid = median.box[YLOW];
    } else {
        xMid = (box[XHIGH] + box[XLOW]) / 2.0;
        yMid = (box[YHIGH] + box[YLOW]) / 2.0;
    }

    vector<float> northWest = {box[XLOW], yMid, xMid, box[YHIGH]};
    children[NW] = new QuadTreeNode(northWest, level + 1);

    vector<float> northEast = {xMid, yMid, box[XHIGH], box[YHIGH]};
    children[NE] = new QuadTreeNode(northEast, level + 1);

    vector<float> southWest = {box[XLOW], box[YLOW], xMid, yMid};
    children[SW] = new QuadTreeNode(southWest, level + 1);

    vector<float> southEast = {xMid, box[YLOW], box[XHIGH], yMid};
    children[SE] = new QuadTreeNode(southEast, level + 1);
}

bool QuadTreeNode::intersects(Record q) {
    return !(box[XLOW] > q.box[XHIGH] || q.box[XLOW] > box[XHIGH] || box[YLOW] > q.box[YHIGH] ||
             q.box[YLOW] > box[YHIGH]);
}

void QuadTreeNode::rangeQuery(Record q, vector<float> &resultItemsIds, map<string, double> &stats) {
    if (isLeaf()) {
        if (intersects(q)) {
            stats["leaf"]++;
            for (auto r : data) {
                if (q.intersects(r)) {
                    //cout << r.id << " " << r.box[XLOW] << " " << r.box[YLOW] << endl;
                    resultItemsIds.push_back(r.id);
                }
            }
        }
        return;
    } else {
        stats["directory"]++;
        for (auto c : children) {
            if (c->intersects(q))
                c->rangeQuery(q, resultItemsIds, stats);
        }
    }
}

void QuadTreeNode::pointQuery(Record q, float &resultItemId, map<string, double> &stats) {
    if (isLeaf()) {
        if (intersects(q)) {
            stats["leaf"]++;
            for (auto r : data) {
                if (q.samePosition(r)) {
                    cout << "Found Point: " << r.id << " " << r.box[XLOW] << " " << r.box[YLOW] << endl;
                    resultItemId = r.id;
                }
            }
        }
        return;
    } else {
        stats["directory"]++;
        for (auto c : children) {
            if (c->intersects(q))
                c->pointQuery(q, resultItemId, stats);
        }
    }
}

typedef struct knnPoint {
    array<float, 2> pt;
    double dist = FLT_MAX;
    int id;
    bool operator<(const knnPoint &second) const { return dist < second.dist; }
} knnPoint;

typedef struct knnNode {
    QuadTreeNode *sn;
    double dist = FLT_MAX;
    bool operator<(const knnNode &second) const { return dist > second.dist; }
} knnNode;

double QuadTreeNode::minSqrDist(array<float, 4> r) const {
    auto b = this->box;
    bool left = r[XHIGH] < b[XLOW];
    bool right = b[XHIGH] < r[XLOW];
    bool bottom = r[YHIGH] < b[YLOW];
    bool top = b[YHIGH] < r[YLOW];
    if (top) {
        if (left)
        // corner distance
            return dist(b[XLOW], b[YHIGH], r[XHIGH], r[YLOW]);
        if (right)
        // corner distance

            return dist(b[XHIGH], b[YHIGH], r[XLOW], r[YLOW]);
        // edge distance
        return (r[YLOW] - b[YHIGH]) * (r[YLOW] - b[YHIGH]);
    }
    if (bottom) {
        if (left)
            return dist(b[XLOW], b[YLOW], r[XHIGH], r[YHIGH]);
        if (right)
            return dist(b[XHIGH], b[YLOW], r[XLOW], r[YHIGH]);
        return (b[YLOW] - r[YHIGH]) * (b[YLOW] - r[YHIGH]);
    }
    if (left)
        // edge distance
        return (b[XLOW] - r[XHIGH]) * (b[XLOW] - r[XHIGH]);
    if (right)
        // edge distance
        return (r[XLOW] - b[XHIGH]) * (r[XLOW] - b[XHIGH]);
    // intersects
    return 0;
}

void QuadTreeNode::kNNQuery(array<float, 2> q, map<string, double> &stats, int k) {
    auto calcSqrDist = [](array<float, 4> x, array<float, 2> y) {
        return pow((x[0] - y[0]), 2) + pow((x[1] - y[1]), 2);
    };

    vector<knnPoint> tempPts(k);
    array<float, 4> query{q[0], q[1], q[0], q[1]};
    priority_queue<knnPoint, vector<knnPoint>> knnPts(all(tempPts));
    priority_queue<knnNode, vector<knnNode>> unseenNodes;
    unseenNodes.emplace(knnNode{this, minSqrDist(query)});
    double dist, minDist;
    QuadTreeNode *node;

    while (!unseenNodes.empty()) {
        node = unseenNodes.top().sn;
        dist = unseenNodes.top().dist;
        unseenNodes.pop();
        // top() returns the largest value
        minDist = knnPts.top().dist;
        if (dist < minDist) {
            if (node->isLeaf()) {
                for (auto p : node->data) {
                    minDist = knnPts.top().dist;
                    dist = calcSqrDist(query, p.toKNNPoint());
                    if (dist < minDist) {
                        knnPoint kPt;
                        kPt.pt = p.toKNNPoint();
                        kPt.dist = dist;
                        kPt.id = p.id;
                        knnPts.pop();
                        knnPts.push(kPt);
                    }
                }
                stats["leaf"]++;
            } else {
                minDist = knnPts.top().dist;
                for (auto c : node->children) {
                    dist = c->minSqrDist(query);
                    if (dist < minDist) {
                        knnNode kn;
                        kn.sn = c;
                        kn.dist = dist;
                        unseenNodes.push(kn);
                    }
                }
                stats["directory"]++;
            }
        } else
            break;
    }
	// prints the results
    /*while (!knnPts.empty()) {
        cout << knnPts.top().pt[0] << " " << knnPts.top().pt[1] << " dist: " << knnPts.top().dist
             << " id:" << knnPts.top().id << endl;
        knnPts.pop();
    }*/
}

void QuadTreeNode::snapshot() {
    ofstream log("QuadTree.csv", ios_base::app);
    log << level << "," << isLeaf() << "," << data.size() << "," << box[XLOW] << "," << box[YLOW]
        << "," << box[XHIGH] << "," << box[YHIGH] << endl;
    log.close();

    if (!isLeaf()) {
        for (auto c : children)
            c->snapshot();
    }
}

void QuadTreeNode::count(int &p, int &d, int &dpc, int &pc) {
    if (isLeaf()) {
        p++;
        dpc += data.size();
        return;
    }
    d++;
    pc += children.size();

    for (auto c : children)
        c->count(p, d, dpc, pc);
}

void QuadTreeNode::calculateSize(int &s) {
    s += sizeof(int) + sizeof(float) * 4; // height  and rectangle
    if (isLeaf())
        return;
    else
        s += 4 * 8; // pointer size

    for (auto c : children)
        c->calculateSize(s);
}

void QuadTreeNode::getTreeHeight(int &h) {
    if (isLeaf()) {
        if (level > h)
            h = level;
        return;
    }

    for (auto c : children)
        c->getTreeHeight(h);
}

void QuadTreeNode::deleteTree() {
    if (isLeaf()) {
        for (auto c : children)
            c->deleteTree();
    }
    delete this;
}

// void QuadTreeNode::getStatistics() {
//     int size = 0, height = 0, pages = 0, directories = 0, dataPoints = 0, pointers = 0;
//     calculateSize(size);
//     getTreeHeight(height);
//     count(pages, directories, dataPoints, pointers);
//     if (POINT_SPLIT)
//         cout << "Strategy: Optimized Point-Quad-Tree" << endl;
//     else
//         cout << "Strategy: Point-Region-Quad-Tree" << endl;
//     cout << "Capacity: " << CAPACITY << endl;
//     cout << "Size in MB: " << size / float(1e6) << endl;
//     cout << "Height: " << height << endl;
//     cout << "Pages: " << pages << endl;
//     cout << "Directories: " << directories << endl;
//     cout << "Data points: " << dataPoints << endl;
//     cout << "Internal pointers: " << pointers << endl;
//     // snapshot();
// }

void QuadTreeNode::getStatistics() {
    int size = 0, height = 0, pages = 0, directories = 0, dataPoints = 0, pointers = 0;
    calculateSize(size);
    getTreeHeight(height);
    count(pages, directories, dataPoints, pointers);

    string strategy = POINT_SPLIT ? "Optimized Point-Quad-Tree" : "Point-Region-Quad-Tree";

    // cout << "{\n";
    cout << "  \"strategy\": \"" << strategy << "\",\n";
    cout << "  \"capacity\": " << CAPACITY << ",\n";
    cout << "  \"sizeInMB\": " << size / float(1e6) << ",\n";
    cout << "  \"height\": " << height << ",\n";
    cout << "  \"pages\": " << pages << ",\n";
    cout << "  \"directories\": " << directories << ",\n";
    cout << "  \"dataPoints\": " << dataPoints << ",\n";
    cout << "  \"internalPointers\": " << pointers << "\n";
    // cout << "}\n";
    // snapshot();
}

QuadTreeNode::~QuadTreeNode() {}

void QuadTree::bulkInsert(Input queries, map<string, double> &log, int method, int level) {

    int total_num = 0;
    int miss_num = 0;

    if (method == 0) { // naive
        for (auto q : queries)
        {
            this->root->insert(q);
        }
    }
    else if (method == 1) { // try last leaf first, if fail insert from root
        if (level == 0) {
            QuadTreeNode* last_leaf = this->root;
            // int total_num = 0;
            // int miss_num = 0;
            for (auto q : queries) {
                total_num++;
                last_leaf = last_leaf->insert(q);
                if (last_leaf == nullptr) {
                    last_leaf = this->root->insert(q); // will not return nullptr
                    miss_num++;
                }
            }
            // cout<<"Total inserts: "<<total_num<<" Miss inserts: "<<miss_num<<endl;
        }
        else {
            QuadTreeNode *last_parent = this->root;
            // int total_num = 0;
            // int miss_num = 0;
            queue<QuadTreeNode *> parentQueue({this->root});
            for (auto q : queries)
            {
                total_num++;
                last_parent = parentQueue.front();
                parentQueue.pop();
                last_parent = last_parent->insert(q, parentQueue, level);
                if (last_parent == nullptr)
                {
                    last_parent = this->root->insert(q, parentQueue, level); // will not return nullptr
                    miss_num++;
                }
            }
            // cout << "Total inserts: " << total_num << " Miss inserts: " << miss_num << endl;
        }
    }
    else if (method == 2) {
        // based on 1. try last leaf -> tranverse
        // add: cache. Save cache_size leaves in the cache

        int cache_size = 3;
        list<QuadTreeNode*> cache;

        if (level == 0) {
            QuadTreeNode* leaf;
            // int total_num = 0;
            // int miss_num = 0;
            for (auto q : queries) {
                total_num++;

                bool hit = false;
                for (auto it = cache.begin(); it != cache.end(); ++it) {
                    leaf = *it;
                    leaf = leaf->insert(q);
                    if (leaf != nullptr) {
                        hit = true;
                        // Move the node to the front of the cache
                        cache.erase(it);
                        cache.push_front(leaf);
                        break;
                    }
                }

                if (!hit) {
                    // Cache miss, insert at root
                    miss_num++;
                    leaf = root->insert(q); // Insert at root and get new node
                    if (leaf) {
                        if (cache.size() >= cache_size) {
                            cache.pop_back(); // Remove the least recently used node if cache is full
                        }
                        cache.push_front(leaf); // Add new node to the front of the cache
                    }
                }
            }
            // cout<<"Total inserts: "<<total_num<<" Miss inserts: "<<miss_num<<endl;
        }
        else {

            QuadTreeNode *leaf;
            QuadTreeNode *parent;
            // int total_num = 0;
            // int miss_num = 0;
            queue<QuadTreeNode *> parentQueue({this->root});  // used to find parent

            for (auto q : queries)
            {
                total_num++;

                bool hit = false;
                for (auto it = cache.begin(); it != cache.end(); ++it) {
                    parent = *it;
                    leaf = parent->insert(q, parentQueue, level);
                    if (leaf != nullptr) {
                        hit = true;
                        // Move the node to the front of the cache
                        parent = parentQueue.front();
                        parentQueue.pop();

                        cache.erase(it);
                        cache.push_front(parent);
                        break;
                    }
                }

                if (!hit) {
                    // Cache miss, insert at root
                    miss_num++;
                    leaf = root->insert(q, parentQueue, level); // Insert at root and get new node
                    if (leaf) {
                        if (cache.size() >= cache_size) {
                            cache.pop_back(); // Remove the least recently used node if cache is full
                        }
                        parent = parentQueue.front();
                        parentQueue.pop();
                        cache.push_front(parent); // Add new node to the front of the cache
                    }
                }
            }
            // cout << "Total inserts: " << total_num << " Miss inserts: " << miss_num << endl;
        }

    }
    else { // naive
        for (auto q : queries)
        {
            this->root->insert(q);
        }
    }

    if (method == 1 || method == 2) {
        cout << "\"Total inserts\": " << total_num << ",\n";
        cout << "\"Miss inserts\": " << miss_num << ", \n";
        cout << "\"Hit rate\": " << (total_num - miss_num) / total_num << ",\n";
    }
}

void QuadTreeNode::exportBoundaries(ofstream& file) {
    if (!isLeaf()) {
        // For non-leaf nodes, write their boundary and recurse
        file << box[XLOW] << "," << box[YLOW] << "," << box[XHIGH] << "," << box[YHIGH] << std::endl;
        for (auto child : children) {
            if (child) child->exportBoundaries(file);
        }
    }
}

void QuadTree::exportTree(const string& filename) {
    ofstream file(filename);
    if (root) {
        root->exportBoundaries(file);
    }
    file.close();
}

