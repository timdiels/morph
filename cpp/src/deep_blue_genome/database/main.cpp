/*
 * Copyright (C) 2015 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
 *
 * This file is part of Deep Blue Genome.
 *
 * Deep Blue Genome is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Deep Blue Genome is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Deep Blue Genome.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <deep_blue_genome/database/stdafx.h>
#include <deep_blue_genome/common/util.h>
#include <deep_blue_genome/common/database_all.h>
#include <deep_blue_genome/database/commands.h>

using namespace std;
using namespace DEEP_BLUE_GENOME;
using namespace DEEP_BLUE_GENOME::DATABASE;

int main(int argc, char** argv) {
	graceful_main([argc, argv](){
		string db_path = "";

		// Read args
		namespace po = boost::program_options;

		po::options_description desc("Allowed options");
		desc.add_options()
		    ("help", "produce help message")
		    ("create", po::value<string>()->value_name("yaml_update_file"), "Create database using a yaml update description file")
			("add", po::value<string>()->value_name("yaml_update_file"), "Add to database using a yaml update description file. Does not overwrite data upon name collision.")
			("dump", po::value<string>()->value_name("dump_file")->implicit_value("database_dump.yaml"), "Dump database to file")
			("database-path", po::value<string>(&db_path)->required(), "Path to directory where database is or should be stored")
			("verify", "Check database integrity")
		;

		auto print_help = [&desc]() {
			cout << "Usage: database [options] database-path"<< "\n";
			cout << "\n";
			cout << desc << "\n";
		};

		try {
			po::positional_options_description positional;
			positional.add("database-path", 1);

			po::variables_map vm;
			po::store(po::command_line_parser(argc, argv).
					  options(desc).positional(positional).run(), vm);

			if (vm.count("help")) {
				print_help();
				return 0;
			}

			po::notify(vm);

			// Execute given command
			if (vm.count("create")) {
				database_create(db_path, vm["create"].as<string>());
			}
			else if (vm.count("add")) {
				database_add(db_path, vm["add"].as<string>());
			}
			else if (vm.count("dump")) {
				database_dump(db_path, vm["dump"].as<string>());
			}
			else if (vm.count("verify")) {
				database_verify(db_path);
			}
			else {
				print_help();
			}
		}
		catch (const po::error& ex) {
			cerr << ex.what() << "\n\n";
			print_help();
			return 1;
		}

		return 0;
	});
}