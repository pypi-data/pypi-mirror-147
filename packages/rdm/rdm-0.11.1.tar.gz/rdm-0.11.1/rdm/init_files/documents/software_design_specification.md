---
id: SDS-001
revision: 1
title: Software Design Specification
---

# Purpose

This document describes *how* {{device.name}} shall fulfill the requirements described in the software requirements specification. It discusses the computation hardware the software will be expected run on, the software system's architecture, functional specifications associated with each software requirement, and user interface mockups.

It is written primarily for engineers working on {{device.name}}, who have the source code available, in addition to this document.

[[The legacy Software option of 62304:4.4 is not in use here.]]

[[FDA-SW:sds]]

# Scope

This document applies to {{device.name}} release {{device.version}}.

# Definitions

The **Food and Drug Administration (FDA)** is a United State government agency responsible for protecting the public health by ensuring the safety, efficacy, and security of human and veterinary drugs, biological products, and medical devices.

The **Health Insurance Portability and Accountability Act** (HIPAA) is a United States law designed to provide privacy standards to protect patients' medical records and other health information provided to health plans, doctors, hospitals and other healthcare providers.

**Protected Health Information** (PHI) means individually identifiable information that is created by {{device.name}} and relates to the past, present, or future physical or mental health or condition of any individual, the provision of health care to an individual, or the past, present, or future payment for the provision of health care to an individual.

**UI** is an acronym for user interface.

# System and Software Architecture Diagrams

The purpose of these diagrams are to present a high-level overview of the device design to facilitate a clear understanding of

1. the software items and hardware components that make up the system
2. the relationships among them
3. the data inputs/outputs and flow of data among them
4. how users or external products, including IT infrastructure and peripherals, interact with the system.

TODO: Add various diagrams to this section (e.g., block, state, flow, sequence, etc.) showing a detailed depiction of functional units and software items. Focus on the high risk parts of the application. The diagrams should be largely self-explanatory without additional context. The diagrams should contain references to the other parts of the SDS. If the device includes other software functions, i.e., functionality that is not itself a medical device, these should be clearly delineated. SOUP and OTS software items should also be delineated in the diagrams.

See [Section VI.C](https://innolitics.com/articles/premarket-submissions-for-device-software-functions/#c-system-and-software-architecture-diagram) for additional guidance about the content and formatting of these diagrams, and [Appendix B](https://innolitics.com/articles/premarket-submissions-for-device-software-functions/#appendix-b-system-and-software-architecture-diagram-chart-examples) for examples.

ENDTODO

[[FDA-SW:ssad]]

# Software Items

TODO: Enumerate the various software items that your system comprises of, and document the design of each one.

## Software Item A

## Software Item B

# SOUP Software Items

This section enumerates the SOUP software items present within {{device.name}}.

{% for s in soup %}
## {{s.title}}

**Manufacturer:**
{% if s.manufacturer is defined %}
{{s.manufacturer}}
{% else %}
SOUP was developed collaboratively by the free open-source software community, and does not have a manufacturer in the traditional sense.
{% endif %}
**Version:**

`{{s.version}}`
{% if device.safety_class != "A" %}
**Functional and Performance Requirements:**

{{s.purpose}}

**Hardware & Software Requirements:**
{% if s.requirements is defined %}
{{s.requirements}}
{% else %}
No noteworthy software or hardware requirements.
{% endif %}
**Known Anomalies:**
{% if s.anomaly_reference is not defined %}
Known anomaly list is not available.
{% else %}
{% if s.relevant_anomalies is not defined %}
No anomalies found that would result in incorrect behaviour for {{device.name}} leading to a hazardous situation.
{% else %}
{{s.anomalies}}
{% endif %}
**Open Anomaly List (Reference Only):**

`{{s.anomaly_reference}}`
{%- endif %}
{%- endif %}
{% endfor %}

# Functional Specifications
{% for requirement in requirements %}
## {{requirement.title}}

*Requirement ID:* {{requirement.id}}

*Requirement:* {{requirement.description}}
{% if 'specifications' in requirement %}

*Functional Specifications:*
{{requirement.specifications}}
{%- endif %}
{%- endfor %}

# User Interface Mockups

TODO: 

If you have user interface mockups, this is a good place to put them. One strategy is to include a sub-section for each screen, along with its own image file. Here are some examples:

## Screen One (PNG)

Use something like: `![Screen One](./images/uimockups/example-ui-mockup-001.png)`

Which produces:

![Screen One](./images/uimockups/example-ui-mockup-001.png)

## Screen Two (JPG)

Use something like: `![Screen Two](./images/uimockups/example-ui-mockup-002.jpg)`

Which produces:

![Screen Two](./images/uimockups/example-ui-mockup-002.jpg)

## Screen Three (PNG Online)

Use something like: `![Screen Three](https://github.com/innolitics/rdm/raw/a29fed650e55b376157cebe8843b087209a0b92a/rdm/init_files/images/uimockups/example-ui-mockup-001.png)`

Which produces:

![Screen Three](https://github.com/innolitics/rdm/raw/a29fed650e55b376157cebe8843b087209a0b92a/rdm/init_files/images/uimockups/example-ui-mockup-001.png)

ENDTODO