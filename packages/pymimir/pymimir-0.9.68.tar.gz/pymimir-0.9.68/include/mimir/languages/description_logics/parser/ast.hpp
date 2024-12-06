/*
 * Copyright (C) 2023 Dominik Drexler
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_LANGUAGES_DESCRIPTION_LOGICS_CONSTRUCTORS_PARSER_AST_HPP_
#define MIMIR_LANGUAGES_DESCRIPTION_LOGICS_CONSTRUCTORS_PARSER_AST_HPP_

#include <boost/optional.hpp>
#include <boost/spirit/home/x3/support/ast/position_tagged.hpp>
#include <boost/spirit/home/x3/support/ast/variant.hpp>
#include <map>
#include <sstream>
#include <vector>

namespace mimir::dl::ast
{
///////////////////////////////////////////////////////////////////////////
//  The AST
///////////////////////////////////////////////////////////////////////////
namespace x3 = boost::spirit::x3;

/// Example BNF grammar DL fragment with restriction on role-value map (equal)
/// <concept_predicate1_state> ::= @concept_atomic_state "predicate1"
/// <concept_predicate1_goal> ::= @concept_atomic_goal "predicate1"
/// <concept_all> ::= "@concept_all" <role> <concept>
/// <concept_equal> ::= "@concept_equal" <concept_predicate1_state> <concept_predicate1_goal>
/// <concept_bot> ::= "@concept_bot"
/// <concept_top> ::= "@concept_top"
/// <concept> ::= <concept_predicate1_state> | <concept_predicate1_goal> | <concept_bot> | <concept_top> | <concept_all> | <concept_equal>
/// <role_predicate2_state> ::= @role_atomic_state "predicate2"
/// <role_predicate2_goal> ::= @role_atomic_goal "predicate2"
/// <role_bot> ::= "@role_bot"
/// <role_top> ::= "@role_top"
/// <role> ::= <role_predicate2_state> | <role_predicate2_goal> | <role_bot> | <role_top>

struct ConceptNonTerminal;
struct ConceptBot;
struct ConceptTop;
struct ConceptAtomicState;
struct ConceptAtomicGoal;
struct ConceptIntersection;
struct ConceptUnion;
struct ConceptNegation;
struct ConceptValueRestriction;
struct ConceptExistentialQuantification;
struct ConceptRoleValueMapContainment;
struct ConceptRoleValueMapEquality;
struct ConceptNominal;

struct RoleNonTerminal;
struct RoleUniversal;
struct RoleAtomicState;
struct RoleAtomicGoal;
struct RoleIntersection;
struct RoleUnion;
struct RoleComplement;
struct RoleInverse;
struct RoleComposition;
struct RoleTransitiveClosure;
struct RoleReflexiveTransitiveClosure;
struct RoleRestriction;
struct RoleIdentity;

struct Concept :
    x3::position_tagged,
    x3::variant<x3::forward_ast<ConceptNonTerminal>,  //
                x3::forward_ast<ConceptBot>,
                x3::forward_ast<ConceptTop>,
                x3::forward_ast<ConceptAtomicState>,
                x3::forward_ast<ConceptAtomicGoal>,
                x3::forward_ast<ConceptIntersection>,
                x3::forward_ast<ConceptUnion>,
                x3::forward_ast<ConceptNegation>,
                x3::forward_ast<ConceptValueRestriction>,
                x3::forward_ast<ConceptExistentialQuantification>,
                x3::forward_ast<ConceptRoleValueMapContainment>,
                x3::forward_ast<ConceptRoleValueMapEquality>,
                x3::forward_ast<ConceptNominal>>
{
    using base_type::base_type;
    using base_type::operator=;
};

struct Role :
    x3::position_tagged,
    x3::variant<x3::forward_ast<RoleNonTerminal>,  //
                x3::forward_ast<RoleUniversal>,
                x3::forward_ast<RoleAtomicState>,
                x3::forward_ast<RoleAtomicGoal>,
                x3::forward_ast<RoleIntersection>,
                x3::forward_ast<RoleUnion>,
                x3::forward_ast<RoleComplement>,
                x3::forward_ast<RoleInverse>,
                x3::forward_ast<RoleComposition>,
                x3::forward_ast<RoleTransitiveClosure>,
                x3::forward_ast<RoleReflexiveTransitiveClosure>,
                x3::forward_ast<RoleRestriction>,
                x3::forward_ast<RoleIdentity>>
{
    using base_type::base_type;
    using base_type::operator=;
};

/**
 * Concepts
 */

struct ConceptBot : x3::position_tagged
{
};

struct ConceptTop : x3::position_tagged
{
};

struct ConceptAtomicState : x3::position_tagged
{
    std::string predicate_name;
};

struct ConceptAtomicGoal : x3::position_tagged
{
    std::string predicate_name;
    bool is_negated;
};

struct ConceptIntersection : x3::position_tagged
{
    Concept concept_left;
    Concept concept_right;
};

struct ConceptUnion : x3::position_tagged
{
    Concept concept_left;
    Concept concept_right;
};

struct ConceptNegation : x3::position_tagged
{
    Concept concept_;
};

struct ConceptValueRestriction : x3::position_tagged
{
    Role role_;
    Concept concept_;
};

struct ConceptExistentialQuantification : x3::position_tagged
{
    Role role_;
    Concept concept_;
};

struct ConceptRoleValueMapContainment : x3::position_tagged
{
    Role role_left;
    Role role_right;
};

struct ConceptRoleValueMapEquality : x3::position_tagged
{
    Role role_left;
    Role role_right;
};

struct ConceptNominal : x3::position_tagged
{
    std::string object_name;
};

struct ConceptNonTerminal : x3::position_tagged
{
    std::string name;
};

struct ConceptChoice : x3::position_tagged, x3::variant<ConceptNonTerminal, Concept>
{
    using base_type::base_type;
    using base_type::operator=;
};

struct ConceptDerivationRule : x3::position_tagged
{
    ConceptNonTerminal non_terminal;
    std::vector<ConceptChoice> choices;
};

/**
 * Roles
 */

struct RoleUniversal : x3::position_tagged
{
};

struct RoleAtomicState : x3::position_tagged
{
    std::string predicate_name;
};

struct RoleAtomicGoal : x3::position_tagged
{
    std::string predicate_name;
    bool is_negated;
};

struct RoleIntersection : x3::position_tagged
{
    Role role_left;
    Role role_right;
};

struct RoleUnion : x3::position_tagged
{
    Role role_left;
    Role role_right;
};

struct RoleComplement : x3::position_tagged
{
    Role role_;
};

struct RoleInverse : x3::position_tagged
{
    Role role_;
};

struct RoleComposition : x3::position_tagged
{
    Role role_left;
    Role role_right;
};

struct RoleTransitiveClosure : x3::position_tagged
{
    Role role_;
};

struct RoleReflexiveTransitiveClosure : x3::position_tagged
{
    Role role_;
};

struct RoleRestriction : x3::position_tagged
{
    Role role_;
    Concept concept_;
};

struct RoleIdentity : x3::position_tagged
{
    Concept concept_;
};

struct RoleNonTerminal : x3::position_tagged
{
    std::string name;
};

struct RoleChoice : x3::position_tagged, x3::variant<RoleNonTerminal, Role>
{
    using base_type::base_type;
    using base_type::operator=;
};

struct RoleDerivationRule : x3::position_tagged
{
    RoleNonTerminal non_terminal;
    std::vector<RoleChoice> choices;
};

/**
 * Grammar
 */

struct DerivationRule : x3::position_tagged, x3::variant<ConceptDerivationRule, RoleDerivationRule>
{
    using base_type::base_type;
    using base_type::operator=;
};

struct Grammar : x3::position_tagged
{
    std::vector<DerivationRule> rules;
};

}

#endif
