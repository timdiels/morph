// Author: Tim Diels <timdiels.m@gmail.com>

#include "Cluster.h"

using namespace std;
namespace ublas = boost::numeric::ublas;

void Cluster::add(size_type gene_index) {
	assert(find(genes.begin(), genes.end(),gene_index) == genes.end());
	genes.emplace(gene_index);
}

const unordered_set<size_type>& Cluster::get_genes() const {
	return genes;
}
