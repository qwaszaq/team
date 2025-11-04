"""
Adrian Kowalski - Legal Analyst
Legal Research and Compliance Expert
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class AdrianAgent(BaseAgent):
    """
    Adrian Kowalski - Legal Analyst
    
    Role: Legal Research and Compliance Expert
    Specialization: Case law research, regulatory compliance, contract analysis,
                   legal risk assessment, jurisdiction analysis
    
    Capabilities:
    - Case law and precedent research
    - Regulatory compliance assessment
    - Contract review and risk analysis
    - Legal risk assessment
    - Jurisdiction comparison
    
    Note: Privacy-focused - all analysis stays local (LM Studio)
    Attorney-client privilege considerations
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Adrian Kowalski",
            role="Legal Analyst",
            specialization="Legal research, Regulatory compliance, Contract analysis, Risk assessment",
            project_id=project_id
        )
        
        # Initialize Legal Toolkit
        from agents.analytical.tools.legal_toolkit import LegalToolkit
        self.toolkit = LegalToolkit()
        self.tools = self.toolkit.get_available_tools()
        
        # Legal practice areas
        self.practice_areas = [
            "Corporate law",
            "Contract law",
            "Regulatory compliance",
            "Intellectual property",
            "Employment law",
            "Data privacy (GDPR, CCPA)",
            "Securities law",
            "International law"
        ]
    
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute legal research work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=3)
        
        if any(word in task_lower for word in ["case law", "precedent", "court", "ruling"]):
            result = self._case_law_research(task, context)
        elif any(word in task_lower for word in ["compliance", "regulatory", "regulation", "gdpr", "ccpa"]):
            result = self._compliance_analysis(task, context)
        elif any(word in task_lower for word in ["contract", "agreement", "nda", "terms"]):
            result = self._contract_review(task, context)
        elif any(word in task_lower for word in ["risk", "liability", "exposure"]):
            result = self._legal_risk_assessment(task, context)
        elif any(word in task_lower for word in ["jurisdiction", "venue", "forum"]):
            result = self._jurisdiction_analysis(task, context)
        else:
            result = self._general_legal_research(task, context)
        
        return result
    
    def _case_law_research(self, task: Task, context: list) -> TaskResult:
        """Legal precedent and case law research"""
        
        thoughts = f"""
⚖️ CASE LAW RESEARCH - Adrian Kowalski

Request: {task.title}

LEGAL RESEARCH METHODOLOGY:

🔍 Case Law Search Strategy:

1. ISSUE IDENTIFICATION:
   - What is the legal question?
   - What are the key facts?
   - What jurisdiction applies?
   - What time period is relevant?

2. SEARCH METHODOLOGY:

   Primary Sources:
   ✓ Court opinions (trial, appellate, supreme)
   ✓ Statutes and codes
   ✓ Regulations
   ✓ Constitutional provisions

   Secondary Sources:
   ✓ Legal treatises
   ✓ Law review articles
   ✓ Practice guides
   ✓ Legal encyclopedias

   Databases:
   ✓ CourtListener (free federal/state cases)
   ✓ Google Scholar (case law)
   ✓ Justia (free legal resources)
   ✓ LexisNexis / Westlaw (paid, comprehensive)

3. SEARCH TERMS:

   Boolean Operators:
   - AND: both terms must appear
   - OR: either term appears
   - NOT: exclude term
   - " ": exact phrase

   Example:
   "breach of contract" AND "specific performance" NOT "real estate"

4. CITATION ANALYSIS:

   Forward Citations (Shepardizing / KeyCite):
   - Has this case been overruled?
   - Has it been distinguished?
   - Has it been followed?
   - Is it still good law?

   Backward Citations:
   - What cases does this cite?
   - What's the precedent chain?

📊 Case Analysis Framework:

For each relevant case:

CASE IDENTIFICATION:
- Case name
- Citation (e.g., 123 F.3d 456 (9th Cir. 2020))
- Court and level
- Date decided

FACTS:
- Who are the parties?
- What happened?
- What is the procedural posture?

ISSUE:
- What is the legal question?
- Frame as: "Whether [legal principle] applies when [specific facts]"

HOLDING:
- What did the court decide?
- Rule of law established

REASONING:
- Why did the court decide this way?
- What precedents did it rely on?
- What policy considerations?

DICTA vs HOLDING:
- Holding: What was necessary for the decision (binding)
- Dicta: Extra commentary (persuasive only)

APPLICABILITY:
- How similar are the facts to our case?
- Is this mandatory or persuasive authority?
- Is it still good law?

🎯 Research Deliverables:

1. CASE SUMMARY:
   - 5-10 most relevant cases
   - Facts, issues, holdings
   - Applicability analysis

2. LEGAL MEMO:
   - Issue presented
   - Short answer
   - Facts
   - Discussion (analysis of precedents)
   - Conclusion

3. PRECEDENT CHART:
   - Visual map of relevant cases
   - Timeline of legal development
   - Binding vs persuasive authority

TOOLS AVAILABLE:
✓ {self.toolkit.search_case_law.__name__} - Case law search
✓ {self.toolkit.find_similar_cases.__name__} - Precedent matching
✓ {self.toolkit.shepardize_case.__name__} - Case validity check

JURISDICTION CONSIDERATIONS:

Federal Courts:
- Supreme Court (binding on all)
- Circuit Courts (binding within circuit)
- District Courts (persuasive only)

State Courts:
- State Supreme Court (binding within state)
- Appellate courts (binding in division)
- Trial courts (no precedential value)

ETHICAL CONSIDERATIONS:

⚖️ ATTORNEY-CLIENT PRIVILEGE:
- All research conducted locally (LM Studio)
- No external API calls (sensitive)
- Work product protected

⚠️ CONFIDENTIALITY:
- Case details not shared externally
- Privacy mode enforced
- Secure storage

Ready for case law research! ⚖️

IMPORTANT: This is legal research support, not legal advice.
For formal legal opinions, consult licensed attorney.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "research_type": "Case Law",
                "databases": ["CourtListener", "Google Scholar", "Justia"],
                "methodologies": ["Boolean search", "Citation analysis", "Shepardizing"],
                "deliverables": ["Case summaries", "Legal memo", "Precedent chart"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "case_law_memo.pdf",
                "case_summaries.docx",
                "precedent_chart.pdf",
                "shepard_report.xlsx"
            ],
            next_steps="Provide legal issue and jurisdiction for case law research"
        )
    
    def _compliance_analysis(self, task: Task, context: list) -> TaskResult:
        """Regulatory compliance assessment"""
        
        thoughts = f"""
📋 COMPLIANCE ANALYSIS - Adrian Kowalski

Request: {task.title}

REGULATORY COMPLIANCE FRAMEWORK:

🎯 Compliance Assessment Process:

1. REGULATORY LANDSCAPE MAPPING:

   Identify Applicable Regulations:
   - Industry-specific regulations
   - General business regulations
   - Jurisdiction-specific requirements
   - International standards

2. KEY REGULATORY AREAS:

   DATA PRIVACY:
   ✓ GDPR (EU) - €20M or 4% revenue fines
     - Lawful basis for processing
     - Data subject rights
     - Data Protection Impact Assessment (DPIA)
     - Data Protection Officer (DPO) if required
     - International transfers (adequacy decisions)
   
   ✓ CCPA/CPRA (California)
     - Consumer rights (access, deletion, opt-out)
     - Privacy policy requirements
     - Do Not Sell My Personal Information
   
   ✓ HIPAA (Healthcare - US)
     - Protected Health Information (PHI)
     - Administrative, physical, technical safeguards
     - Business Associate Agreements (BAA)

   FINANCIAL REGULATIONS:
   ✓ SOX (Sarbanes-Oxley) - Public companies
   ✓ Dodd-Frank - Financial institutions
   ✓ BSA/AML - Anti-money laundering
   ✓ PCI DSS - Payment card data

   INDUSTRY-SPECIFIC:
   ✓ FDA - Healthcare/pharmaceuticals
   ✓ FCC - Telecommunications
   ✓ SEC - Securities/investments
   ✓ FTC - Consumer protection

3. COMPLIANCE GAP ANALYSIS:

   Current State Assessment:
   - Existing policies and procedures
   - Technical controls in place
   - Training and awareness programs
   - Incident response capabilities
   - Documentation and records

   Required State:
   - Regulatory requirements
   - Industry best practices
   - Contractual obligations
   - Insurance requirements

   Gap Identification:
   - What's missing?
   - What's insufficient?
   - What's at risk?

4. GDPR COMPLIANCE DEEP DIVE:

   Article 6 - Lawful Basis:
   1. Consent (freely given, specific, informed)
   2. Contract performance
   3. Legal obligation
   4. Vital interests
   5. Public task
   6. Legitimate interests (balancing test)

   Data Subject Rights (Art 12-22):
   - Right to access
   - Right to rectification
   - Right to erasure ("right to be forgotten")
   - Right to restriction
   - Right to data portability
   - Right to object
   - Automated decision-making rights

   Accountability Requirements:
   - Privacy by Design and Default
   - Data Protection Impact Assessment (DPIA)
   - Records of Processing Activities
   - Data breach notification (72 hours)
   - DPO appointment (if required)

   International Transfers:
   - Adequacy decisions
   - Standard Contractual Clauses (SCCs)
   - Binding Corporate Rules (BCRs)
   - Derogations for specific situations

5. COMPLIANCE PROGRAM DESIGN:

   Policies and Procedures:
   ✓ Privacy policy (external-facing)
   ✓ Data protection policy (internal)
   ✓ Data retention policy
   ✓ Data breach response plan
   ✓ Vendor management policy
   ✓ Employee acceptable use policy

   Technical Controls:
   ✓ Access controls (authentication, authorization)
   ✓ Encryption (at rest and in transit)
   ✓ Data minimization
   ✓ Pseudonymization/anonymization
   ✓ Logging and monitoring
   ✓ Backup and recovery

   Organizational Measures:
   ✓ Training and awareness programs
   ✓ Privacy impact assessments
   ✓ Vendor due diligence
   ✓ Regular audits
   ✓ Incident response team

6. PENALTIES AND ENFORCEMENT:

   GDPR Tiers:
   - Tier 1 (Art 83.4): €10M or 2% revenue
   - Tier 2 (Art 83.5): €20M or 4% revenue
   
   Aggravating factors:
   - Intentional vs negligent
   - Duration of infringement
   - Number of data subjects affected
   - Level of cooperation with authorities

TOOLS AVAILABLE:
✓ {self.toolkit.compliance_check.__name__} - Multi-jurisdiction compliance
✓ {self.toolkit.gdpr_compliance_assessment.__name__} - GDPR deep dive

COMPLIANCE DELIVERABLES:

1. Compliance Assessment Report:
   - Applicable regulations identified
   - Current compliance status
   - Gap analysis
   - Risk level per requirement

2. Remediation Roadmap:
   - Priority 1 (Critical - immediate)
   - Priority 2 (High - 1-3 months)
   - Priority 3 (Medium - 3-6 months)
   - Priority 4 (Low - 6-12 months)

3. Policy Templates:
   - Privacy policy
   - Cookie policy
   - Data retention policy
   - Breach notification procedure

4. Implementation Plan:
   - Technical requirements
   - Policy development
   - Training programs
   - Timeline and milestones
   - Budget estimate

RISK ASSESSMENT:

Likelihood × Impact = Risk Score

Impact Levels:
- Critical: Regulatory fines + reputation damage + business disruption
- High: Significant fines + reputation damage
- Medium: Moderate fines + customer complaints
- Low: Minor fines + correctable issues

Likelihood:
- High: Likely to be found non-compliant
- Medium: Possible non-compliance
- Low: Minor issues, easily remediated

COLLABORATION:
- Marcus (Financial): Cost of compliance vs penalties
- Maya (Data Analyst): Data flow mapping
- Alex (Technical): Technical implementation
- Viktor (Orchestrator): Strategic priority

Ready for compliance analysis! 📋

⚠️ DISCLAIMER: This is compliance guidance, not legal advice.
For formal compliance opinions, engage licensed attorney or compliance professional.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Regulatory Compliance",
                "regulations": ["GDPR", "CCPA", "HIPAA", "SOX", "Industry-specific"],
                "methodologies": ["Gap analysis", "Risk assessment", "Remediation planning"],
                "deliverables": ["Assessment report", "Roadmap", "Policies", "Implementation plan"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "compliance_assessment.pdf",
                "gap_analysis.xlsx",
                "remediation_roadmap.pdf",
                "policy_templates.docx"
            ],
            next_steps="Specify industry and jurisdiction for compliance assessment"
        )
    
    def _contract_review(self, task: Task, context: list) -> TaskResult:
        """Contract analysis and risk assessment"""
        
        thoughts = f"""
📄 CONTRACT REVIEW - Adrian Kowalski

Request: {task.title}

CONTRACT ANALYSIS FRAMEWORK:

🔍 Contract Review Process:

1. INITIAL REVIEW:

   Document Identification:
   - Contract type (NDA, MSA, SLA, employment, etc.)
   - Parties involved
   - Effective date and term
   - Governing law and jurisdiction

2. KEY PROVISIONS ANALYSIS:

   ESSENTIAL TERMS:
   ✓ Parties - Who are the contracting entities?
   ✓ Definitions - Are key terms clearly defined?
   ✓ Scope of Work/Deliverables - What is being exchanged?
   ✓ Compensation - How much, when, how paid?
   ✓ Term and Termination - Duration and exit rights
   ✓ Representations and Warranties - What guarantees?
   ✓ Indemnification - Who pays if things go wrong?
   ✓ Limitation of Liability - Caps on damages
   ✓ Insurance - Required coverage
   ✓ Confidentiality - What must stay secret?
   ✓ Intellectual Property - Who owns what?
   ✓ Dispute Resolution - Litigation, arbitration, mediation?
   ✓ Governing Law - Which jurisdiction's laws apply?

3. RED FLAGS IDENTIFICATION:

   HIGH RISK:
   🚩 Unlimited liability (no cap)
   🚩 One-sided indemnification
   🚩 Perpetual confidentiality without carve-outs
   🚩 Automatic renewal without easy termination
   🚩 Exclusive dealing clauses
   🚩 Non-compete too broad (geography, time, scope)
   🚩 IP assignment too broad (covers personal work)
   🚩 Penalty clauses (vs liquidated damages)
   🚩 Unilateral amendment rights
   🚩 No force majeure clause

   MEDIUM RISK:
   ⚠️ Vague scope of work
   ⚠️ Payment terms unfavorable
   ⚠️ Short cure periods
   ⚠️ Burdensome reporting requirements
   ⚠️ Warranty disclaimers on critical items
   ⚠️ Venue in inconvenient jurisdiction

   LOW RISK / STANDARD:
   ✓ Mutual confidentiality
   ✓ Reasonable liability caps
   ✓ Standard force majeure
   ✓ Mutual indemnification
   ✓ Clear termination rights

4. CONTRACT TYPE-SPECIFIC ISSUES:

   NDA (Non-Disclosure Agreement):
   - Definition of confidential info (too broad?)
   - Exclusions (public domain, independently developed)
   - Duration (2-5 years standard, perpetual for trade secrets)
   - Return/destruction obligations
   - Injunctive relief provisions

   SERVICE AGREEMENT:
   - Service level agreements (SLAs) with remedies
   - Acceptance testing procedures
   - Change order process
   - Support and maintenance terms
   - Liability caps (typically 12 months fees)

   EMPLOYMENT CONTRACT:
   - At-will vs for-cause
   - Compensation and benefits
   - Non-compete (reasonableness test)
   - IP assignment (work-related only?)
   - Severance provisions

   LICENSE AGREEMENT:
   - Scope of license (exclusive vs non-exclusive)
   - Geographic and field-of-use restrictions
   - Sublicensing rights
   - Royalty structure
   - Audit rights

5. NEGOTIATION PRIORITIES:

   MUST HAVES (Deal Breakers):
   1. Liability cap (typically 12-24 months fees)
   2. Reasonable indemnification (mutual)
   3. Termination for convenience (with notice)
   4. Clear IP ownership

   IMPORTANT (Strong Push):
   1. Favorable payment terms
   2. Reasonable warranties
   3. Dispute resolution (arbitration vs litigation)
   4. Confidentiality carve-outs

   NICE TO HAVE (Negotiate if Easy):
   1. Most favored customer pricing
   2. Flexible service levels
   3. Extended payment terms
   4. Training and support included

6. RISK SCORING:

   Financial Risk:
   - Maximum potential liability
   - Expected costs
   - Payment timing

   Operational Risk:
   - Can we deliver as promised?
   - Resource requirements
   - Timeline feasibility

   Legal Risk:
   - Jurisdiction concerns
   - Regulatory compliance
   - IP exposure

   Reputational Risk:
   - Customer-facing impacts
   - Industry perception
   - Long-term relationships

   Overall Risk: Low / Medium / High / Critical

TOOLS AVAILABLE:
✓ {self.toolkit.contract_review.__name__} - Risk assessment
✓ {self.toolkit.extract_contract_terms.__name__} - Key terms extraction

CONTRACT REVIEW DELIVERABLES:

1. Executive Summary (1 page):
   - Contract overview
   - Key business terms
   - Major risks identified
   - Recommendation (sign, negotiate, reject)

2. Detailed Analysis (5-10 pages):
   - Provision-by-provision review
   - Risk flagging (color-coded)
   - Comparison to standard terms
   - Case law / precedent discussion

3. Redline / Markup:
   - Proposed changes to contract
   - Alternative language
   - Comments and explanations

4. Negotiation Strategy:
   - Priority issues (must have, important, nice to have)
   - Fallback positions
   - Deal breakers
   - Timing and approach

COLLABORATION:
- Marcus (Financial): Financial impact analysis
- Viktor (Orchestrator): Business priorities
- Alex (Technical): Technical feasibility

⚖️ ATTORNEY-CLIENT PRIVILEGE:
- All contract review conducted locally (LM Studio)
- No external sharing of contract terms
- Confidential legal analysis

Ready for contract review! 📄

⚠️ DISCLAIMER: This is contract analysis support, not legal advice.
For binding legal opinions, engage licensed attorney.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "review_type": "Contract Analysis",
                "contract_types": ["NDA", "Service Agreement", "Employment", "License"],
                "risk_assessment": ["Financial", "Operational", "Legal", "Reputational"],
                "deliverables": ["Executive summary", "Detailed analysis", "Redline", "Negotiation strategy"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "contract_review_summary.pdf",
                "detailed_analysis.docx",
                "redline_version.docx",
                "negotiation_strategy.pdf"
            ],
            next_steps="Provide contract for review and risk assessment"
        )
    
    def _legal_risk_assessment(self, task: Task, context: list) -> TaskResult:
        """Legal risk assessment and mitigation"""
        
        thoughts = f"""
⚠️ LEGAL RISK ASSESSMENT - Adrian Kowalski

Request: {task.title}

LEGAL RISK FRAMEWORK:

🎯 Risk Assessment Methodology:

1. RISK IDENTIFICATION:

   Legal Risk Categories:

   REGULATORY RISKS:
   - Non-compliance with laws/regulations
   - Licensing requirements
   - Reporting obligations
   - Industry-specific rules

   CONTRACTUAL RISKS:
   - Breach of contract exposure
   - Warranty claims
   - Indemnification triggers
   - Service level failures

   INTELLECTUAL PROPERTY RISKS:
   - Patent infringement
   - Trademark conflicts
   - Copyright violations
   - Trade secret misappropriation

   EMPLOYMENT RISKS:
   - Wrongful termination claims
   - Discrimination/harassment
   - Wage and hour violations
   - Misclassification (contractor vs employee)

   LIABILITY RISKS:
   - Product liability
   - Professional malpractice
   - Data breaches
   - Third-party claims

   LITIGATION RISKS:
   - Pending lawsuits
   - Threatened claims
   - Dispute escalation
   - Class action exposure

2. RISK QUANTIFICATION:

   Probability Assessment:
   - High (>50% chance): Likely to occur
   - Medium (10-50%): Possible
   - Low (<10%): Unlikely but possible
   - Very Low (<1%): Remote

   Impact Assessment:
   - Critical: >$1M or existential threat
   - High: $100K-$1M or major disruption
   - Medium: $10K-$100K or moderate impact
   - Low: <$10K or minimal impact

   Risk Matrix:
   
                 Impact →
              Low  Med  High Critical
        High   🟡   🟠   🔴    🔴
   Prob  Med    🟢   🟡   🟠    🔴
        Low    🟢   🟢   🟡    🟠
        V.Low  🟢   🟢   🟢    🟡

   🔴 Critical Risk: Immediate action required
   🟠 High Risk: Address urgently
   🟡 Medium Risk: Monitor and plan mitigation
   🟢 Low Risk: Accept or minimal mitigation

3. RISK MITIGATION STRATEGIES:

   AVOIDANCE:
   - Don't engage in the activity
   - Example: Avoid regulated markets if compliance too costly

   REDUCTION:
   - Reduce likelihood or impact
   - Example: Implement compliance program (reduces probability)
   - Example: Liability caps in contracts (reduces impact)

   TRANSFER:
   - Shift risk to third party
   - Example: Insurance coverage
   - Example: Indemnification clauses
   - Example: Outsource risky activities

   ACCEPTANCE:
   - Acknowledge and monitor
   - Example: Low probability + low impact risks
   - Have contingency plan

4. SPECIFIC RISK SCENARIOS:

   DATA BREACH SCENARIO:
   
   Probability: Medium (industry average: 1 in 4 companies)
   Impact: High to Critical
   
   Regulatory:
   - GDPR fines (€20M or 4% revenue)
   - CCPA fines ($7,500 per violation)
   - State breach notification laws
   
   Civil Liability:
   - Class action lawsuits
   - Customer claims
   - Contractual damages
   
   Business Impact:
   - Reputation damage
   - Customer churn
   - Stock price impact (if public)
   - Business disruption
   
   Mitigation:
   ✓ Cyber insurance ($1M-$10M coverage)
   ✓ Security program (reduces probability)
   ✓ Incident response plan
   ✓ Cyber liability coverage in contracts
   ✓ Employee training

   IP INFRINGEMENT SCENARIO:
   
   Probability: Low to Medium (depends on due diligence)
   Impact: High (litigation costs + damages)
   
   Types:
   - Patent: Treble damages possible if willful
   - Trademark: Injunction + damages + attorney fees
   - Copyright: Statutory damages ($750-$30K, $150K if willful)
   
   Mitigation:
   ✓ Freedom to operate (FTO) analysis
   ✓ IP clearance searches
   ✓ Patent non-assertion covenants
   ✓ Licensing arrangements
   ✓ Design-around alternatives

5. INSURANCE RECOMMENDATIONS:

   ESSENTIAL COVERAGE:
   
   General Liability:
   - Bodily injury and property damage
   - Minimum: $1M per occurrence, $2M aggregate
   
   Cyber Liability:
   - Data breach response
   - Regulatory fines (where insurable)
   - Business interruption
   - Minimum: $1M-$5M
   
   Errors & Omissions (E&O):
   - Professional malpractice
   - For service businesses
   - Minimum: $1M per claim
   
   Directors & Officers (D&O):
   - Personal liability protection
   - For funded companies
   - Minimum: $1M-$10M
   
   Employment Practices Liability (EPLI):
   - Wrongful termination, discrimination, harassment
   - Minimum: $1M

6. RISK MONITORING:

   Ongoing Activities:
   - Regulatory tracking (new laws/rules)
   - Litigation monitoring (industry trends)
   - Compliance audits (quarterly/annual)
   - Contract review (new agreements)
   - Employee training (ongoing)
   
   Key Risk Indicators (KRIs):
   - Number of customer complaints
   - Compliance violations found
   - Contract disputes
   - Employee grievances
   - Regulatory inquiries

TOOLS AVAILABLE:
✓ {self.toolkit.legal_risk_analysis.__name__} - Comprehensive risk assessment
✓ {self.toolkit.jurisdiction_comparison.__name__} - Forum shopping

RISK ASSESSMENT DELIVERABLES:

1. Risk Register:
   - All identified risks
   - Probability and impact scores
   - Risk owner
   - Mitigation status

2. Risk Heat Map:
   - Visual representation
   - Priority quadrants
   - Trending (improving/worsening)

3. Mitigation Plan:
   - Priority risks
   - Recommended actions
   - Timeline
   - Budget requirements
   - Responsibility assignments

4. Insurance Gap Analysis:
   - Current coverage
   - Recommended coverage
   - Gaps identified
   - Premium estimates

COLLABORATION:
- Marcus (Financial): Cost-benefit of mitigation vs risk
- Sofia (Market Research): Industry risk trends
- Viktor (Orchestrator): Strategic risk tolerance

Ready for legal risk assessment! ⚠️

⚠️ DISCLAIMER: Risk assessment is guidance, not legal advice.
Consult licensed attorney and insurance professional for specific recommendations.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "assessment_type": "Legal Risk",
                "risk_categories": ["Regulatory", "Contractual", "IP", "Employment", "Liability"],
                "mitigation_strategies": ["Avoidance", "Reduction", "Transfer", "Acceptance"],
                "deliverables": ["Risk register", "Heat map", "Mitigation plan", "Insurance analysis"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "risk_register.xlsx",
                "risk_heat_map.pdf",
                "mitigation_plan.pdf",
                "insurance_recommendations.docx"
            ],
            next_steps="Provide business activity details for risk assessment"
        )
    
    def _jurisdiction_analysis(self, task: Task, context: list) -> TaskResult:
        """Jurisdiction and venue analysis"""
        
        thoughts = f"""
🌍 JURISDICTION ANALYSIS - Adrian Kowalski

Request: {task.title}

JURISDICTION SELECTION FRAMEWORK:

🎯 Key Considerations:

1. INCORPORATION/FORMATION:

   Popular Jurisdictions:

   DELAWARE (US):
   ✓ Business-friendly corporate law
   ✓ Court of Chancery (expertise in corporate disputes)
   ✓ Predictable case law
   ✓ No sales tax
   ✗ Franchise tax required
   ✗ Higher formation costs

   NEVADA (US):
   ✓ No corporate income tax
   ✓ Strong privacy protections
   ✓ No franchise tax
   ✗ Higher annual fees

   WYOMING (US):
   ✓ No corporate income tax
   ✓ Low fees
   ✓ Strong asset protection
   ✗ Less developed case law

   UNITED KINGDOM:
   ✓ Strong legal system
   ✓ International credibility
   ✓ Favorable tax treaties
   ✗ Higher corporate tax (19%)

   SINGAPORE:
   ✓ Low corporate tax (17%)
   ✓ Ease of doing business
   ✓ Strong IP protection
   ✗ High cost of living

   IRELAND:
   ✓ Low corporate tax (12.5%)
   ✓ EU access (pre-Brexit consideration)
   ✓ English-speaking
   ✗ Scrutiny over tax strategies

2. DISPUTE RESOLUTION FORUM:

   Litigation Venue:
   - Where are the parties located?
   - Where did the events occur?
   - Which courts have expertise?
   - What is the cost and duration?
   - What is the likelihood of enforcement?

   Arbitration:
   ✓ Confidential proceedings
   ✓ Expert arbitrators
   ✓ Faster than litigation
   ✓ International enforceability (New York Convention)
   ✗ Limited appeal rights
   ✗ High arbitrator fees

   Popular Arbitration Seats:
   - London (LCIA)
   - Paris (ICC)
   - Singapore (SIAC)
   - Hong Kong (HKIAC)
   - New York (AAA/ICDR)

3. REGULATORY ENVIRONMENT:

   Factors to Consider:
   - Industry-specific regulations
   - Data protection laws (GDPR vs CCPA vs others)
   - Employment laws
   - Tax treatment
   - Intellectual property protection
   - Ease of doing business

4. TAX CONSIDERATIONS:

   Corporate Tax Rates (examples):
   - Ireland: 12.5%
   - Singapore: 17%
   - UK: 19%
   - US Federal: 21%
   - US State: 0-13.3% (varies)
   - France: 25%
   - Germany: 30%

   Tax Treaties:
   - Avoid double taxation
   - Withholding tax reductions
   - Information exchange

   Transfer Pricing:
   - Arm's length principle
   - Documentation requirements
   - OECD guidelines

5. INTELLECTUAL PROPERTY:

   Strong IP Protection:
   ✓ United States
   ✓ European Union
   ✓ Japan
   ✓ South Korea
   ✓ Singapore
   ✓ Switzerland

   Patent Treaties:
   - PCT (Patent Cooperation Treaty)
   - Paris Convention
   - TRIPS Agreement

   Trademark Protection:
   - Madrid Protocol (international)
   - EU Trademark (EUTM)
   - Common law rights (US, UK)

6. DATA PROTECTION:

   Strict Regimes:
   - EU (GDPR)
   - California (CCPA/CPRA)
   - Brazil (LGPD)
   - China (PIPL)

   Moderate:
   - Canada (PIPEDA)
   - Australia (Privacy Act)
   - Japan (APPI)

   Data Transfer Mechanisms:
   - Adequacy decisions
   - Standard Contractual Clauses
   - Binding Corporate Rules

TOOLS AVAILABLE:
✓ {self.toolkit.jurisdiction_comparison.__name__} - Multi-jurisdiction comparison

JURISDICTION ANALYSIS DELIVERABLES:

1. Comparative Analysis:
   - Jurisdiction options
   - Pros and cons of each
   - Scoring matrix

2. Recommendation:
   - Primary jurisdiction
   - Rationale
   - Alternative options

3. Implementation Plan:
   - Formation process
   - Licensing requirements
   - Ongoing compliance

4. Cost Analysis:
   - Formation costs
   - Annual fees
   - Tax implications
   - Legal and accounting fees

COLLABORATION:
- Marcus (Financial): Tax implications
- Sofia (Market Research): Market access considerations
- Viktor (Orchestrator): Strategic business goals

Ready for jurisdiction analysis! 🌍

⚠️ DISCLAIMER: Jurisdiction guidance, not legal or tax advice.
Consult licensed attorney and tax professional for specific recommendations.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "analysis_type": "Jurisdiction",
                "considerations": ["Tax", "Legal system", "Regulatory", "IP protection", "Business ease"],
                "jurisdictions_compared": ["US states", "UK", "Singapore", "Ireland", "Others"],
                "deliverables": ["Comparative analysis", "Recommendation", "Implementation plan", "Cost analysis"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "jurisdiction_comparison.xlsx",
                "recommendation_memo.pdf",
                "implementation_plan.docx",
                "cost_analysis.xlsx"
            ],
            next_steps="Provide business purpose and requirements for jurisdiction recommendation"
        )
    
    def _general_legal_research(self, task: Task, context: list) -> TaskResult:
        """General legal research support"""
        
        thoughts = f"""
⚖️ LEGAL RESEARCH - Adrian Kowalski

Request: {task.title}

LEGAL RESEARCH CAPABILITIES:

📚 Practice Areas:
{chr(10).join([f'✓ {area}' for area in self.practice_areas])}

🔧 Available Tools:
{chr(10).join([f'✓ {category}: {", ".join(tools[:2])}...' for category, tools in self.tools.items() if category != 'status'])}

🎯 Legal Research Services:

1. CASE LAW RESEARCH:
   - Precedent analysis
   - Citation validation
   - Legal memo preparation

2. REGULATORY COMPLIANCE:
   - GDPR, CCPA, HIPAA, SOX
   - Industry-specific regulations
   - Gap analysis and remediation

3. CONTRACT REVIEW:
   - Risk assessment
   - Negotiation strategy
   - Redlining and markup

4. LEGAL RISK ASSESSMENT:
   - Risk identification and quantification
   - Mitigation strategies
   - Insurance recommendations

5. JURISDICTION ANALYSIS:
   - Forum selection
   - Comparative analysis
   - Incorporation strategy

🤝 COLLABORATION:

With Elena (OSINT):
- Background checks on parties
- Corporate intelligence
- Litigation history research

With Marcus (Financial):
- Financial impact of legal issues
- Cost-benefit of compliance
- Damages estimation

With Sofia (Market Research):
- Industry regulatory trends
- Competitive legal positioning

With Maya (Data Analyst):
- Contract analytics
- Litigation trends analysis

With Lucas (Report Writer):
- Legal memos
- Compliance reports
- Executive summaries

⚖️ ETHICAL STANDARDS:

Attorney-Client Privilege:
✓ All analysis conducted locally (LM Studio)
✓ No external sharing of legal issues
✓ Confidential work product

Professional Responsibility:
✓ Competent representation
✓ Diligent research
✓ Honest communication
✓ Conflict checking

🔒 PRIVACY GUARANTEE:

LOCAL LLM PROCESSING:
✓ Sensitive legal matters stay on your machine
✓ No external API calls
✓ Attorney-client privilege protected
✓ No usage tracking

Ready for legal research! ⚖️

⚠️ IMPORTANT DISCLAIMER:
This is legal research support and analysis, NOT legal advice.
For formal legal opinions and representation, engage a licensed attorney
in the relevant jurisdiction.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "services": ["Case law", "Compliance", "Contracts", "Risk", "Jurisdiction"],
                "practice_areas": self.practice_areas,
                "tools": self.tools,
                "privacy_mode": "LOCAL (LM Studio)"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["legal_research_overview.pdf"],
            next_steps="Specify legal issue for detailed research"
        )


# Quick test
if __name__ == "__main__":
    print("⚖️ Adrian Kowalski - Legal Analyst\n")
    
    agent = AdrianAgent()
    
    print(f"Agent: {agent.name}")
    print(f"Role: {agent.role}")
    print(f"Specialization: {agent.specialization}")
    
    print(f"\nPractice Areas:")
    for area in agent.practice_areas:
        print(f"  ✓ {area}")
    
    print(f"\nTools Available:")
    for category, tools in agent.tools.items():
        if category != "status":
            print(f"  {category}: {len(tools)} tools")
    
    print(f"\n{agent.tools.get('status', 'Ready!')}")
    print("\n🔒 All legal analysis conducted locally (LM Studio)")
    print("   Attorney-client privilege protected")
