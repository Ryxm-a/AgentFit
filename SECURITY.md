# Security Policy

## Reporting a vulnerability

Please do not publish exploitable security issues in a public GitHub issue. Use GitHub's private vulnerability reporting feature for this repository when available, or contact the repository owner privately through their GitHub profile.

Include the affected version, reproduction steps, impact, and any suggested mitigation. Please avoid accessing data that is not yours or testing against third-party systems without authorization.

## Trust model

AgentFit consumes metadata from external registries and repositories. That data is untrusted. AgentFit therefore treats generated installation plans as reviewable output and does not automatically execute third-party install commands.

An AgentFit recommendation is not a security certification. Users should review source code, requested permissions, package provenance and generated commands before installing third-party software.
