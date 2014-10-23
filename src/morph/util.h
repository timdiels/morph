/*
 * Copyright (C) 2014 by Tim Diels
 *
 * This file is part of binreverse.
 *
 * binreverse is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * binreverse is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with binreverse.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <sstream>
#include <fstream>
#include <map>
#include <functional>

// This class taken from: http://stackoverflow.com/a/25351759/1031434
// Contributed by Jason R
class make_string
{
public:
	make_string()
	{
	}

    template <typename T>
    explicit make_string(T && rhs)
    {
        oss << rhs;
    }

    template <typename T>
    make_string &operator<<(T && rhs)
    {
        oss << rhs;
        return *this;
    }

    operator std::string() const
    {
        return oss.str();
    }

    std::string str() const
    {
        return oss.str();
    }

private:
    std::ostringstream oss;
};

/**
 * Find greatest key smaller than given key
 */
template <class K, class V>
typename std::map<K,V>::const_iterator infimum(const std::map<K, V>& map_, const K& value) {
	auto it = map_.upper_bound(value);
	assert (it != map_.begin());
	it--;
	return it;
}

/**
 * Open file for reading, call reader when it's open
 */
void read_file(std::string path, std::function<void(std::ifstream&)> reader);


template<class Container, class T>
bool contains(const Container& container, const T& value) {
	return std::find(container.begin(), container.end(), value) != container.end();
}

