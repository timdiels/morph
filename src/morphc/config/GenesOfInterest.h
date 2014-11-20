// Author: Tim Diels <timdiels.m@gmail.com>

#pragma once

#include <string>
#include <vector>
#include <yaml-cpp/yaml.h>

namespace MORPHC {
namespace CONFIG {

class GenesOfInterest
{
public:
	GenesOfInterest(std::string data_root, YAML::Node genes_of_interest);
	const std::vector<std::string>& get_genes() const;
	std::string get_name() const;

private:
	std::string name;
	std::vector<std::string> genes;
};

}}