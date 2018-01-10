# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of MORPH.
#
# MORPH is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MORPH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MORPH.  If not, see <http://www.gnu.org/licenses/>.

# TODO test everything. See cedalion.badirate's tests for an example. First unit
# test (i.e. in isolation); then test combinations of units or the whole,
# optionally mocking units used which have already been tested. Still it's good
# to also have a functional test of the whole without mocking; it's impractical
# to cover all cases using a test like this, consider it a sample, it usually
# does uncover some more bugs. Especially think of edge cases when unit testing, e.g.
# baits being mapped to the same gene (it's valid for a gene mapping to map 2
# names to 1 e.g. MSU-RAP does this sometimes) may cause trouble with things
# that expect a unique set of baits (e.g. forgetting to call set() on the
# mapping result).
# Use dummy data to keep repo size small and tests easy to edit later on.