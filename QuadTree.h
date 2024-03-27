#ifndef QUADTREE_QUADTREE_H
#define QUADTREE_QUADTREE_H

#include "Input.h"
#include <bits/stdc++.h>
#include "def.h"

using namespace std;

class QuadTreeNode{
public :
    vector<QuadTreeNode*> children = vector<QuadTreeNode*>(4);
    Input data;
    int level;
    vector<float> box;

    QuadTreeNode(vector<float> boundary, int level);
    void insert(Record);
    void bulkInsert(Input queries, map<string, double> &log);
    bool intersects(Record r);
    void rangeQuery(Record q, vector<float> &results, map<string, double> &map);
    void pointQuery(Record q, float &result, map<string, double> &map);
    void kNNQuery(array<float, 2> p, map<string, double> &stats, int k);
    void deleteTree();
    void calculateSize(int &);
    void getTreeHeight(int &);
    void snapshot();
    double minSqrDist(array<float, 4> r) const;
    void packing(Input &R);
    void packing();
    void divide();
    void count(int &, int &, int &, int &);
    bool isLeaf();
    void getStatistics();
    ~QuadTreeNode();
};

class QuadTree{
public:
    QuadTreeNode * root;
    QuadTree(vector<float> boundary, int level) { root = new QuadTreeNode(boundary, 0); };
    void insert(Record r) { return root->insert(r); };
    void bulkInsert(Input queries, map<string, double> &log) { return root->bulkInsert(queries, log); };
    bool intersects(Record r){ return root->intersects(r);};
    void rangeQuery(Record q, vector<float> &results, map<string, double> &map) { return root->rangeQuery(q, results, map); };
    void pointQuery(Record q, float &result, map<string, double> &map) { return root->pointQuery(q, result, map); };
    void kNNQuery(array<float, 2> p, map<string, double> &stats, int k) { return root->kNNQuery(p, stats, k); };
    void deleteTree() { return root->deleteTree(); };
    void calculateSize(int &i) { return root->calculateSize(i); };
    void getTreeHeight(int &i) { return root->getTreeHeight(i); };
    void snapshot() { return root->snapshot(); };
    double minSqrDist(array<float, 4> r) const {return root->minSqrDist(r);};
    void packing(Input &R) { return root->packing(R); };
    void packing() { return root->packing(); };
    void divide() { return root->divide(); };
    void count(int &i1, int &i2, int &i3, int &i4) { return root->count(i1, i2, i3, i4); };
    bool isLeaf() { return root->isLeaf(); };
    void getStatistics() { return root->getStatistics(); };
    ~QuadTree(){delete(root);};
};

#endif //QUADTREE_QUADTREE_H
