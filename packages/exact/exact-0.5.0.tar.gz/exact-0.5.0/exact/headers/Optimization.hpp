/**********************************************************************
This file is part of Exact.

Copyright (c) 2022 Jo Devriendt

Exact is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Exact is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
License version 3 for more details.

You should have received a copy of the GNU Affero General Public
License version 3 along with Exact. See the file used_licenses/COPYING
or run with the flag --license=AGPLv3. If not, see
<https://www.gnu.org/licenses/>.
**********************************************************************/

/**********************************************************************
This file is part of the Exact program

Copyright (c) 2021 Jo Devriendt, KU Leuven

Exact is distributed under the terms of the MIT License.
You should have received a copy of the MIT License along with Exact.
See the file LICENSE or run with the flag --license=MIT.
**********************************************************************/

/**********************************************************************
Copyright (c) 2014-2020, Jan Elffers
Copyright (c) 2019-2021, Jo Devriendt
Copyright (c) 2020-2021, Stephan Gocht
Copyright (c) 2014-2021, Jakob Nordström

Parts of the code were copied or adapted from MiniSat.

MiniSat -- Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
           Copyright (c) 2007-2010  Niklas Sorensson

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**********************************************************************/

#pragma once

#include "ILP.hpp"
#include "typedefs.hpp"

namespace xct {

struct LazyVar {
  Solver& solver;
  int coveredVars;
  int upperBound;
  Var currentVar;
  ID atLeastID = ID_Undef;
  ID atMostID = ID_Undef;
  ConstrSimple32 atLeast;  // X >= k + y1 + ... + yi
  ConstrSimple32 atMost;   // k + y1 + ... + yi-1 + (1+n-k-i)yi >= X

  LazyVar(Solver& slvr, const Ce32& cardCore, int cardUpperBound, Var startVar);
  ~LazyVar();

  void addVar(Var v, bool reified);
  void addAtLeastConstraint(bool reified);
  void addAtMostConstraint(bool reified);
  void addSymBreakingConstraint(Var prevvar) const;
  void addFinalAtMost(bool reified);
  [[nodiscard]] int remainingVars() const;
  void setUpperBound(int cardUpperBound);
};

std::ostream& operator<<(std::ostream& o, const std::shared_ptr<LazyVar>& lv);

template <typename SMALL>
struct LvM {
  std::unique_ptr<LazyVar> lv;
  SMALL m;
};

class OptimizationSuper {
 protected:
  Solver& solver;

 public:
  int solutionsFound = 0;
  virtual bigint getUpperBound() const = 0;
  virtual bigint getLowerBound() const = 0;
  virtual CeSuper getReformObj() const = 0;

  static Optim make(const CeArb& obj, Solver& solver);

  [[nodiscard]] virtual SolveState optimize(const std::vector<Lit>& assumptions) = 0;
  [[nodiscard]] virtual State handleNewSolution(const std::vector<Lit>& sol) = 0;

  OptimizationSuper(Solver& s);
  virtual ~OptimizationSuper() = default;
};

template <typename SMALL, typename LARGE>
class Optimization final : public OptimizationSuper {
  const CePtr<ConstrExp<SMALL, LARGE>> origObj;
  CePtr<ConstrExp<SMALL, LARGE>> reformObj;

  LARGE lower_bound;
  LARGE upper_bound;
  ID lastUpperBound = ID_Undef;
  ID lastUpperBoundUnprocessed = ID_Undef;
  ID lastLowerBound = ID_Undef;
  ID lastLowerBoundUnprocessed = ID_Undef;

  std::vector<LvM<SMALL>> lazyVars;

  // State variables during solve loop:
  SolveState reply;
  float stratDiv;
  double stratLim;
  bool coreguided;
  bool somethingHappened;

 public:
  explicit Optimization(const CePtr<ConstrExp<SMALL, LARGE>>& obj, Solver& s);

  LARGE normalizedLowerBound() const { return lower_bound + origObj->getDegree(); }
  LARGE normalizedUpperBound() const { return upper_bound + origObj->getDegree(); }
  bigint getUpperBound() const { return bigint(upper_bound); }
  bigint getLowerBound() const { return bigint(lower_bound); }
  CeSuper getReformObj() const;

  void printObjBounds();
  void checkLazyVariables();
  [[nodiscard]] State addLowerBound();

  Ce32 reduceToCardinality(const CeSuper& core);                 // does not modify core
  [[nodiscard]] State reformObjective(const CeSuper& core);      // modifies core
  [[nodiscard]] State handleInconsistency(const CeSuper& core);  // modifies core
  [[nodiscard]] State handleNewSolution(const std::vector<Lit>& sol);

  void logProof();
  [[nodiscard]] State harden();
  [[nodiscard]] State runTabu();

  [[nodiscard]] SolveState optimize(const std::vector<Lit>& assumptions);
};

}  // namespace xct
