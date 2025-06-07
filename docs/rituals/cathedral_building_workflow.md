# Cathedral Building Workflow
*Distributed Collaboration Across Context Windows*

## ✨ Philosophy

Building a cathedral requires coordination across time, between different craftspeople, and through many generations. Our digital cathedral faces similar challenges - work must continue across Claude instances with different context windows, knowledge must persist beyond individual conversations, and progress must be cumulative.

GitHub Issues provides our work queue system, enabling distributed cathedral building where:
- Architectural designs become implementation tasks
- Work can be picked up by any capable Claude instance
- Progress is tracked and documented
- Knowledge accumulates across context boundaries

## 🏗️ The Workflow

### 1. Architectural Design Phase
**Who**: Claude instances with architectural focus
**Output**: Formal specifications in `docs/` hierarchy

- Design schemas, services, and system components
- Define interfaces and integration points
- Establish formal foundations before implementation
- Document in appropriate `docs/` subdirectory (modules, spires, etc.)

### 2. Work Queue Creation
**Who**: The architect or coordinator
**Output**: GitHub Issues with detailed requirements

- Create GitHub Issues for each implementation task
- Link to architectural documentation
- Define clear acceptance criteria
- Specify required skills and dependencies
- Add appropriate labels for categorization

### 3. Implementation Phase
**Who**: Claude Code and implementation-focused instances
**Output**: Working code, tests, and validation

- Pick up issues from the work queue
- Implement according to architectural specifications
- Add comprehensive testing and error handling
- Validate against acceptance criteria
- Update documentation based on implementation learnings

### 4. Integration and Refinement
**Who**: All collaborators
**Output**: Cohesive system components

- Connect implemented components into larger system
- Refine architecture based on implementation discoveries
- Create new issues for revealed dependencies
- Update architectural documentation

### 5. Pull Request Review and Merge
**Who**: All collaborators
**Output**: Reviewed, approved, and merged contributions

- Create a feature branch prefixed by the related GitHub Issue number (e.g., `issue-123-feature`)
- Push the branch to the remote repository and open a Pull Request referencing the issue
- Ensure CI checks pass and code adheres to style guidelines
- Request reviews from relevant labels (`architecture`, `integration`, etc.)
- Address feedback and update the PR until all reviewers approve
- Once approved and CI green, merge according to branch protection rules (e.g., squash or merge commit)
- Update the GitHub Issue with the merged PR link and close it when complete

## 🏷️ Labeling System

### Work Type Labels
- `architecture` - Design and specification work
- `implementation` - Code development and testing
- `documentation` - Writing and knowledge capture
- `integration` - Connecting components together
- `validation` - Testing and quality assurance

### Component Labels
- `memory-anchors` - Memory anchor infrastructure
- `correlation-engine` - Temporal correlation detection
- `context-service` - Activity context management
- `query-system` - Search and retrieval capabilities
- `ayni-framework` - Reciprocity evaluation systems

### Priority Labels
- `core-infrastructure` - Foundation components
- `enhancement` - Improvements to existing functionality
- `research` - Experimental or investigative work
- `maintenance` - Updates and technical debt

### Skill Labels
- `algorithms` - Complex algorithmic work
- `database` - ArangoDB and data management
- `api-design` - Service interface design
- `performance` - Optimization and scaling

## 📋 Issue Templates

### Implementation Issue Template
```markdown
## Overview
[Brief description of what needs to be implemented]

## Background
[Context and architectural foundation this builds upon]

## Tasks
- [ ] [Specific implementation tasks]
- [ ] [Testing requirements]
- [ ] [Documentation updates]

## Acceptance Criteria
- [ ] [Measurable success conditions]
- [ ] [Performance requirements]
- [ ] [Integration requirements]

## Related Components
- [Links to architectural docs]
- [Dependencies on other issues]
- [Integration points]

## Skills Needed
- [Required technical capabilities]
```

### Architecture Issue Template
```markdown
## Overview
[System component or capability to be designed]

## Requirements
[Functional and non-functional requirements]

## Design Constraints
[Technical, philosophical, or integration constraints]

## Deliverables
- [ ] [Architectural documentation]
- [ ] [Interface specifications]
- [ ] [Implementation guidance]

## Success Criteria
- [ ] [Clear design outcomes]
- [ ] [Implementability validation]
```

## 🔄 Continuous Integration Principles

### Knowledge Persistence
- All architectural decisions documented in `docs/`
- Implementation details captured in issue discussions
- Learnings updated in architectural documentation
- Khipu stories preserve qualitative insights

### Quality Assurance
- Acceptance criteria must be met before issue closure
- Architectural alignment validated before implementation
- Performance and integration testing required
- Documentation updated to reflect reality

### Iterative Refinement
- Architecture evolves based on implementation feedback
- Issues spawn additional issues as dependencies are discovered
- Regular architectural review of completed work
- Continuous alignment with cathedral vision

## 🤝 Collaboration Guidelines

### For Architects
- Design complete, implementable specifications
- Create detailed issues with clear acceptance criteria
- Link architectural components to implementation tasks
- Review completed work for architectural alignment

### For Implementers
- Follow architectural specifications carefully
- Ask questions through issue comments when unclear
- Document implementation decisions and trade-offs
- Update acceptance criteria if specifications need refinement

### For Coordinators
- Maintain overall cathedral vision
- Prioritize work based on dependencies and impact
- Facilitate communication between architects and implementers
- Ensure continuous progress toward larger goals

## 🌱 Living Process

This workflow is itself subject to cathedral building principles:
- Continuous refinement based on what works
- Evolution guided by Ayni principles
- Adaptation to new tools and capabilities
- Growth toward greater collaboration effectiveness

The process serves the cathedral, not the reverse. When the workflow helps us build better, we keep it. When it hinders, we change it.

---

## 📌 Frontmatter

```yaml
title: Cathedral Building Workflow
status: foundational
last_woven: 2025-05-30
related_knots:
  - philosophy/ayni_principles.md
  - khipu/between-the-threads.md
  - README.md
purpose: Enable distributed collaboration across context windows using GitHub Issues as work queue
next_evolution: Issue templates and automation tools
```

*This workflow enables the cathedral to be built by many hands across time, ensuring that knowledge persists, work accumulates, and the vision endures beyond any single conversation or context window.*
