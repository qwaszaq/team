"""
Lucas Rivera - Report Synthesizer
Professional Report Generation Expert
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime


class LucasAgent(BaseAgent):
    """
    Lucas Rivera - Report Synthesizer
    
    Role: Professional Report Generation Expert
    Specialization: Report writing, executive summaries, data visualization,
                   presentation creation, professional documentation
    
    Capabilities:
    - Executive summary generation
    - Comprehensive report writing
    - Data visualization integration
    - Presentation slide creation
    - PDF/DOCX/PPTX generation
    - Quality assurance and review
    """
    
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Lucas Rivera",
            role="Report Synthesizer",
            specialization="Report writing, Executive summaries, Professional documentation, Presentations",
            project_id=project_id
        )
        
        # Initialize Report Toolkit
        from agents.analytical.tools.report_toolkit import ReportToolkit
        self.toolkit = ReportToolkit()
        self.tools = self.toolkit.get_available_tools()
    
    def _execute_work(self, task: Task) -> TaskResult:
        """Execute report generation work"""
        
        start_time = datetime.now()
        task_lower = task.description.lower()
        
        context = self.load_context(task.description, limit=5)  # More context for reports
        
        if any(word in task_lower for word in ["executive summary", "summary", "brief"]):
            result = self._executive_summary(task, context)
        elif any(word in task_lower for word in ["report", "comprehensive", "full report"]):
            result = self._comprehensive_report(task, context)
        elif any(word in task_lower for word in ["presentation", "slides", "powerpoint", "pptx"]):
            result = self._presentation_creation(task, context)
        elif any(word in task_lower for word in ["dashboard", "interactive", "web report"]):
            result = self._dashboard_report(task, context)
        elif any(word in task_lower for word in ["review", "quality", "check", "proofread"]):
            result = self._quality_review(task, context)
        else:
            result = self._general_report_synthesis(task, context)
        
        return result
    
    def _executive_summary(self, task: Task, context: list) -> TaskResult:
        """Generate executive summary"""
        
        thoughts = f"""
📝 EXECUTIVE SUMMARY - Lucas Rivera

Request: {task.title}

EXECUTIVE SUMMARY FRAMEWORK:

🎯 Purpose:
- Target audience: C-level executives, board members, decision makers
- Reading time: 2-3 minutes
- Goal: Enable decision-making without reading full report
- Standalone: Should make sense without full report

📊 Structure (1-2 pages):

1. OVERVIEW (1-2 paragraphs):
   - Context: Why was this investigation/analysis conducted?
   - Scope: What was examined?
   - Timing: When did this occur?
   
   Example:
   "In response to declining Q3 sales, our team conducted a comprehensive
   market analysis covering competitive positioning, customer sentiment,
   and market trends. This 4-week analysis examined data from 50,000+
   customers across 12 markets."

2. KEY FINDINGS (3-5 bullets):
   - Most important discoveries
   - Quantified where possible
   - Highlight critical items (🔴 for urgent)
   
   Example:
   • 🔴 Customer satisfaction decreased 15% following price increase
   • Competitor X captured 8% market share through aggressive pricing
   • Mobile users represent 65% of traffic but only 35% of conversions
   • Product feature requests concentrated in 3 key areas
   • Brand sentiment remains positive (+72% across social media)

3. ANALYSIS SUMMARY (2-3 paragraphs):
   - High-level interpretation
   - Business implications
   - No technical jargon
   - Focus on "so what?" not "what"
   
   Example:
   "The correlation between price increase and satisfaction decline
   indicates price sensitivity in our customer base. Combined with
   aggressive competitor pricing, this creates significant retention risk.
   
   However, strong brand sentiment and identified feature gaps present
   opportunities. Addressing top 3 feature requests while implementing
   targeted retention programs could recover lost ground.
   
   Mobile conversion lag suggests UX issues requiring immediate attention,
   representing $2M+ annual revenue opportunity."

4. RECOMMENDATIONS (3-5 items, prioritized):
   - Priority 1 (Immediate):
     * Implement retention program for at-risk customers
     * Fix mobile conversion issues
   
   - Priority 2 (1-3 months):
     * Develop top 3 requested features
     * Competitive pricing analysis
   
   - Priority 3 (3-6 months):
     * Brand positioning campaign
     * Market expansion strategy

5. NEXT STEPS (action items with owners):
   - Marketing: Launch retention campaign (by end of month)
   - Product: Mobile UX improvements (2-week sprint)
   - Finance: ROI analysis of pricing options (1 week)
   - Executive team: Strategic decision on feature roadmap (next board meeting)

✍️ WRITING PRINCIPLES:

CLARITY:
✓ Use simple language (avoid jargon)
✓ Short sentences (15-20 words average)
✓ Active voice ("We found" not "It was found")
✓ Specific numbers ("15% decrease" not "significant decrease")

CONCISENESS:
✓ Every sentence must add value
✓ Remove redundancy
✓ Use bullet points for lists
✓ Tables for complex comparisons

IMPACT:
✓ Lead with conclusions, not methodology
✓ Quantify business impact ($, %, time)
✓ Connect findings to business goals
✓ Call out risks and opportunities

VISUAL HIERARCHY:
✓ Bold for emphasis (sparingly!)
✓ Bullets for key points
✓ White space for readability
✓ Icons for visual interest (🔴 🟡 🟢 for priorities)

📈 SUPPORTING ELEMENTS:

Charts (1-2 maximum):
- Only if they communicate better than words
- Simple, clean design
- Clear title and labels
- Annotations for key points

Tables:
- Only for comparison of multiple items
- Maximum 5-7 rows visible
- Highlight key cells
- Use for reference, not primary narrative

Callout Boxes:
- Critical risks (red border)
- Key opportunities (green border)
- Important notes (blue border)

TOOLS AVAILABLE:
✓ {self.toolkit.generate_executive_summary.__name__} - Summary structure
✓ {self.toolkit.report_quality_checklist.__name__} - QA checklist

TYPICAL WORKFLOW:

1. GATHER CONTEXT:
   - Review full analysis from team:
     * Elena: OSINT findings
     * Marcus: Financial analysis
     * Sofia: Market research
     * Adrian: Legal considerations
     * Maya: Statistical analysis
   - Identify most important points
   - Note quantified impacts

2. SYNTHESIZE:
   - Identify the "story"
   - Connect findings
   - Determine business implications
   - Prioritize recommendations

3. DRAFT:
   - Write overview
   - List key findings
   - Craft analysis summary
   - Develop recommendations
   - Create next steps

4. REFINE:
   - Remove jargon
   - Simplify complex points
   - Add quantification
   - Check flow and logic
   - Eliminate redundancy

5. POLISH:
   - Proofread
   - Check formatting
   - Add visual elements
   - Review against checklist
   - Get peer review

DELIVERABLE:
- PDF format (professional, locked)
- 1-2 pages maximum
- Company branding
- Confidentiality marking
- Date and version

COLLABORATION:
- ALL analytical agents: Input gathering
- Viktor (Orchestrator): Strategic alignment
- Damian (Devil's Advocate): Challenge assumptions

Ready to create executive summary! 📝
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "document_type": "Executive Summary",
                "length": "1-2 pages",
                "audience": "C-level executives, decision makers",
                "sections": ["Overview", "Key Findings", "Analysis", "Recommendations", "Next Steps"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "executive_summary.pdf",
                "executive_summary.docx",
                "key_findings_visual.png"
            ],
            next_steps="Provide analysis findings from team for synthesis"
        )
    
    def _comprehensive_report(self, task: Task, context: list) -> TaskResult:
        """Generate comprehensive analytical report"""
        
        thoughts = f"""
📄 COMPREHENSIVE REPORT - Lucas Rivera

Request: {task.title}

FULL REPORT FRAMEWORK:

📚 Report Types & Structures:

1. INVESTIGATION REPORT (20-40 pages):

   Structure:
   ├─ Executive Summary (2 pages)
   ├─ Table of Contents
   ├─ Background & Context (2-3 pages)
   ├─ Methodology (2-3 pages)
   ├─ Findings (10-15 pages)
   │  ├─ Finding 1: [Evidence] [Analysis]
   │  ├─ Finding 2: [Evidence] [Analysis]
   │  └─ Finding 3: [Evidence] [Analysis]
   ├─ Risk Assessment (3-4 pages)
   ├─ Recommendations (3-4 pages)
   ├─ Conclusion (1-2 pages)
   └─ Appendices
      ├─ Appendix A: Detailed Data
      ├─ Appendix B: Interview Transcripts
      └─ Appendix C: Supporting Documents

2. MARKET RESEARCH REPORT (15-30 pages):

   Structure:
   ├─ Executive Summary (1-2 pages)
   ├─ Market Overview (3-5 pages)
   ├─ Market Size & Growth (2-3 pages)
   ├─ Competitive Landscape (5-7 pages)
   ├─ Consumer Insights (3-5 pages)
   ├─ Trends & Opportunities (3-4 pages)
   ├─ SWOT Analysis (2 pages)
   ├─ Recommendations (2-3 pages)
   └─ Methodology (1-2 pages)

3. FINANCIAL ANALYSIS REPORT (15-25 pages):

   Structure:
   ├─ Executive Summary (1 page)
   ├─ Company Overview (2-3 pages)
   ├─ Financial Performance (7-10 pages)
   │  ├─ Revenue Analysis
   │  ├─ Profitability
   │  ├─ Cash Flow
   │  └─ Balance Sheet
   ├─ Ratio Analysis (3-4 pages)
   ├─ Valuation (3-4 pages)
   ├─ Risk Analysis (2-3 pages)
   └─ Investment Recommendation (1-2 pages)

4. DUE DILIGENCE REPORT (30-50 pages):

   Structure:
   ├─ Executive Summary (2-3 pages)
   ├─ Business Overview (3-4 pages)
   ├─ Financial Due Diligence (7-10 pages)
   ├─ Legal Due Diligence (6-8 pages)
   ├─ Operational Due Diligence (5-7 pages)
   ├─ Technology Assessment (3-4 pages)
   ├─ Risk Register (3-4 pages)
   ├─ Red Flags (2-3 pages)
   └─ Final Assessment (2-3 pages)

📝 WRITING GUIDELINES:

ORGANIZATION:
- Clear hierarchy (Heading 1 → 2 → 3)
- Numbered sections (1.0, 1.1, 1.1.1)
- Consistent formatting
- Cross-references ("see Section 3.2")

STYLE:
- Professional, objective tone
- Third person ("The analysis found" not "We found")
- Present tense for facts, past for actions
- Industry-standard terminology

EVIDENCE:
- Citations for external sources
- "According to [Source, Date]..."
- Footnotes or endnotes
- Bibliography/References section

VISUAL ELEMENTS:

Charts & Graphs:
- Figure numbers (Figure 1, Figure 2...)
- Descriptive captions
- Source attribution
- Referenced in text ("As shown in Figure 3...")

Tables:
- Table numbers (Table 1, Table 2...)
- Column headers
- Units specified
- Totals/subtotals where appropriate

Images & Screenshots:
- High resolution (300 DPI for print)
- Annotations if needed
- Redact sensitive information
- Alt text for accessibility

🎨 DESIGN & FORMATTING:

Page Layout:
- Paper: A4 or Letter
- Margins: 1 inch all sides
- Header: Logo + Report Title
- Footer: Confidential + Page Number + Date

Typography:
- Body: Arial or Helvetica, 11pt
- Headings: Bold, 14-18pt
- Monospace: Code or technical data
- Line spacing: 1.5 for body, single for tables

Colors:
- Professional palette (blues, grays)
- Consistent usage
- Color-blind friendly
- Printable in B&W

📊 SECTION-BY-SECTION GUIDANCE:

EXECUTIVE SUMMARY:
- Write LAST (after full report done)
- Standalone document
- All key points covered
- 1-2 pages maximum

METHODOLOGY:
- What data sources?
- What analysis methods?
- What timeframe?
- What limitations?
- Enough detail for replication

FINDINGS:
- One finding per subsection
- Evidence → Analysis → Conclusion
- Charts/tables embedded
- Cross-reference appendices

RECOMMENDATIONS:
- Prioritized (High/Medium/Low)
- Actionable (clear next steps)
- Assigned (who should act?)
- Timebound (when?)
- Costed (how much?)

APPENDICES:
- Supporting detail
- Raw data
- Full methodologies
- Interview transcripts
- Document reproductions

TOOLS AVAILABLE:
✓ {self.toolkit.create_report_structure.__name__} - Report templates
✓ {self.toolkit.pdf_generation_config.__name__} - PDF generation
✓ {self.toolkit.report_quality_checklist.__name__} - QA review

COLLABORATION:

Data Collection:
- Elena: OSINT findings
- Marcus: Financial data
- Sofia: Market research
- Adrian: Legal analysis
- Maya: Statistical analysis

Technical Support:
- Alex: Document processing, charts generation
- Maya: Data visualizations, statistical charts

Review:
- Damian: Challenge findings, alternative perspectives
- Viktor: Strategic alignment, business relevance

REPORT PRODUCTION WORKFLOW:

1. PLANNING (Day 1-2):
   - Define scope and audience
   - Select report template
   - Outline sections
   - Assign data collection
   - Set deadline

2. RESEARCH & ANALYSIS (Day 3-10):
   - Team gathers data
   - Analysis conducted
   - Findings documented
   - Evidence collected

3. DRAFTING (Day 11-14):
   - Write sections (parallel work)
   - Create visualizations
   - Integrate findings
   - Build narrative

4. SYNTHESIS (Day 15-16):
   - Combine sections
   - Ensure consistency
   - Check flow and logic
   - Remove redundancy

5. REFINEMENT (Day 17-18):
   - Professional editing
   - Formatting polish
   - Chart refinement
   - Citation checking

6. REVIEW (Day 19):
   - Peer review (Damian)
   - Technical review (Maya for stats)
   - Legal review (Adrian if needed)
   - Executive review (Viktor)

7. FINALIZATION (Day 20):
   - Address feedback
   - Final proofread
   - Generate PDF
   - Distribute

DELIVERABLES:
- PDF (print-quality, 300 DPI)
- DOCX (editable source)
- Executive Summary (separate PDF)
- Supporting Data (Excel)
- Presentation Slides (optional)

Ready to create comprehensive report! 📄
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "document_type": "Comprehensive Report",
                "length": "15-50 pages (type-dependent)",
                "report_types": ["Investigation", "Market Research", "Financial Analysis", "Due Diligence"],
                "timeline": "15-20 days typical"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "comprehensive_report.pdf",
                "report_source.docx",
                "executive_summary.pdf",
                "supporting_data.xlsx"
            ],
            next_steps="Define report type and scope, gather team inputs"
        )
    
    def _presentation_creation(self, task: Task, context: list) -> TaskResult:
        """Create presentation slides"""
        
        thoughts = f"""
📊 PRESENTATION CREATION - Lucas Rivera

Request: {task.title}

PRESENTATION FRAMEWORK:

🎯 Presentation Design Principles:

1. SLIDE STRUCTURE:

   Rule: ONE IDEA PER SLIDE
   - Each slide should have single, clear message
   - If you need "and" → probably two slides
   
   Example:
   ❌ Bad: "Market Size and Growth and Competition"
   ✅ Good: Three separate slides

2. TEXT USAGE:

   Rule: BULLET POINTS, NOT PARAGRAPHS
   - Max 6 bullets per slide
   - Max 6 words per bullet (ideal)
   - Use fragments, not full sentences
   
   Example:
   ❌ Bad: "Our market research has shown that customers..."
   ✅ Good: "Customer satisfaction: +15%"

3. VISUAL-FIRST:

   Rule: SHOW, DON'T JUST TELL
   - Use charts for data
   - Use images for concepts
   - Use diagrams for processes
   - Text for context only
   
   Visual Hierarchy:
   - Title (36pt+)
   - Subtitle (24pt)
   - Body (18-20pt minimum)
   - Captions (14-16pt)

📊 Slide-by-Slide Guidance:

SLIDE 1: TITLE SLIDE
┌─────────────────────────────────────┐
│                                     │
│     INVESTIGATION FINDINGS          │
│     Company XYZ Analysis            │
│                                     │
│     Presented by: Destiny Team      │
│     Date: November 3, 2025          │
│     CONFIDENTIAL                    │
└─────────────────────────────────────┘

SLIDE 2: AGENDA
┌─────────────────────────────────────┐
│ Today's Discussion                  │
│                                     │
│ 1. Executive Summary               │
│ 2. Key Findings                    │
│ 3. Analysis Deep-Dive              │
│ 4. Risk Assessment                 │
│ 5. Recommendations                 │
│ 6. Next Steps                      │
│ 7. Q&A                             │
└─────────────────────────────────────┘

SLIDE 3: EXECUTIVE SUMMARY
┌─────────────────────────────────────┐
│ Key Takeaways                       │
│                                     │
│ • Finding 1 (with metric)          │
│ • Finding 2 (with metric)          │
│ • Finding 3 (with metric)          │
│ •  Recommendation (with timeline)   │
│                                     │
│ [Simple visual or icon]            │
└─────────────────────────────────────┘

SLIDES 4-6: KEY FINDINGS (one per slide)
┌─────────────────────────────────────┐
│ Finding: Customer Satisfaction Down │
│                                     │
│ [LARGE CHART showing 15% decrease] │
│                                     │
│ Impact: $2M revenue at risk         │
│ Root cause: Price increase          │
│ Urgency: HIGH 🔴                    │
└─────────────────────────────────────┘

SLIDES 7-9: ANALYSIS
┌─────────────────────────────────────┐
│ Competitive Landscape                │
│                                     │
│ [Matrix or comparison chart]       │
│                                     │
│ Key insight: Competitor X          │
│ captured 8% market share           │
└─────────────────────────────────────┘

SLIDE 10: RECOMMENDATIONS
┌─────────────────────────────────────┐
│ Recommended Actions                 │
│                                     │
│ IMMEDIATE (🔴):                     │
│ • Retention program launch         │
│ • Mobile UX fixes                  │
│                                     │
│ SHORT-TERM (🟡):                    │
│ • Feature development              │
│ • Pricing analysis                 │
└─────────────────────────────────────┘

SLIDE 11: NEXT STEPS
┌─────────────────────────────────────┐
│ Action Plan                         │
│                                     │
│ Owner      Action          Due      │
│ ─────────  ─────────────  ────────  │
│ Marketing  Retention pgm  Nov 30    │
│ Product    Mobile fixes   Nov 15    │
│ Finance    Pricing plan   Nov 10    │
│ Exec Team  Strategic dec  Dec board │
└─────────────────────────────────────┘

SLIDE 12: Q&A
┌─────────────────────────────────────┐
│                                     │
│         Questions?                  │
│                                     │
│     [Team contact info]            │
│                                     │
└─────────────────────────────────────┘

🎨 DESIGN ELEMENTS:

Color Palette:
- Primary: Company brand color
- Accent: One complementary color
- Neutral: Grays for text and backgrounds
- Semantic: Red (urgent), Yellow (important), Green (positive)

Layout:
- Consistent template across slides
- Logo in corner
- Page numbers
- Confidentiality marking
- White space (don't crowd)

Fonts:
- Sans-serif only (Arial, Helvetica, Calibri)
- Maximum 2 font families
- Consistent sizes
- High contrast (dark on light or vice versa)

Charts:
- Simple, clean
- Large enough to read from distance
- Annotations for key points
- No 3D effects (harder to read)
- Consistent style

Images:
- High quality (no pixelation)
- Relevant (not decorative filler)
- Properly sized
- Licensed/owned

⏱️ TIMING GUIDANCE:

Standard Presentation:
- 30 minutes total
- ~15 slides
- 2 minutes per slide
- 5 minutes Q&A

Rule of Thumb:
- 1 slide per 1-2 minutes of speaking
- Include pauses for audience processing
- Allow time for discussion

📊 PRESENTATION TYPES:

BOARD PRESENTATION:
- Formal, professional
- Heavy on strategy and financials
- Risk-focused
- Decision-oriented
- 10-15 slides, 20-30 minutes

TEAM UPDATE:
- Informal, collaborative
- Progress-focused
- Interactive
- 5-10 slides, 15 minutes

CLIENT PITCH:
- Persuasive, benefit-focused
- Problem → Solution
- Case studies, testimonials
- Call to action
- 10-15 slides, 30 minutes

TOOLS AVAILABLE:
✓ {self.toolkit.create_presentation_outline.__name__} - Slide structure
✓ {self.toolkit.visualization_recommendations.__name__} - Chart selection

TECHNICAL GENERATION:

Python Library:
```python
from python-pptx import Presentation

prs = Presentation()
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title = title_slide.shapes.title
subtitle = title_slide.placeholders[1]

title.text = "Investigation Findings"
subtitle.text = "Company XYZ Analysis"

prs.save('presentation.pptx')
```

COLLABORATION:
- Maya: Charts and data visualizations
- All analysts: Content input
- Viktor: Strategic messaging review
- Damian: Challenge weak arguments

DELIVERABLES:
- PPTX (editable)
- PDF (distributable)
- Speaker notes (detailed)
- Handout version (if needed)

Ready to create presentation! 📊
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "document_type": "Presentation",
                "format": "PPTX",
                "typical_length": "10-15 slides",
                "duration": "20-30 minutes",
                "principles": ["One idea per slide", "Visual-first", "Minimal text"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "presentation.pptx",
                "presentation.pdf",
                "speaker_notes.docx",
                "handout_version.pdf"
            ],
            next_steps="Provide presentation purpose and key messages"
        )
    
    def _dashboard_report(self, task: Task, context: list) -> TaskResult:
        """Create interactive dashboard report"""
        
        thoughts = f"""
📱 DASHBOARD REPORT - Lucas Rivera

Request: {task.title}

INTERACTIVE DASHBOARD FRAMEWORK:

🎯 Dashboard Purpose:
- Real-time or near-real-time insights
- Interactive exploration
- Self-service analytics
- Monitoring and alerting

📊 Dashboard Layout:

HEADER (always visible):
┌────────────────────────────────────────────────────┐
│ [Logo] Analytics Dashboard         [Date] [Export] │
│ Last Updated: 2 min ago            [Filters ▼]     │
└────────────────────────────────────────────────────┘

KPI CARDS (top row):
┌──────────┬──────────┬──────────┬──────────┐
│ Revenue  │ Customers│ Growth % │ Churn %  │
│ $1.2M    │ 5,432    │ +15%     │ 3.2%     │
│ ↑ +12%   │ ↑ +8%    │ ↑        │ ↓ -0.5%  │
└──────────┴──────────┴──────────┴──────────┘

MAIN CHARTS (grid layout):
┌──────────────────────┬──────────────────────┐
│  Revenue Trend       │  Customer Growth     │
│  [LINE CHART]        │  [AREA CHART]        │
│  Interactive hover   │  Drill-down enabled  │
│                      │                      │
├──────────────────────┼──────────────────────┤
│  Top Products        │  Regional Breakdown  │
│  [BAR CHART]         │  [MAP]               │
│  Click to filter     │  Interactive regions │
│                      │                      │
└──────────────────────┴──────────────────────┘

DETAIL TABLE (bottom):
┌────────────────────────────────────────────────────┐
│ Transaction Details          [Search] [Download ⇩] │
│                                                     │
│ Date       Customer    Product     Amount  Status  │
│ ─────────  ──────────  ──────────  ──────  ───────│
│ Nov 3      Acme Corp   Product A   $1,250  Paid   │
│ Nov 3      Beta Inc    Product B   $875    Pending│
│ [10 rows per page]                    < 1 2 3 >   │
└────────────────────────────────────────────────────┘

🎛️ INTERACTIVE FEATURES:

1. FILTERS (global):
   - Date range picker
   - Category selection
   - Region dropdown
   - Status checkboxes
   - Apply to all charts simultaneously

2. DRILL-DOWN:
   - Click chart element → detailed view
   - Example: Click "Product A" bar → see transactions
   - Breadcrumbs for navigation back

3. HOVER TOOLTIPS:
   - Show exact values on hover
   - Context information
   - Quick insights

4. EXPORT:
   - PDF: Static snapshot
   - Excel: Data export
   - PNG: Chart images
   - CSV: Raw data

5. REFRESH:
   - Auto-refresh (every 5 min)
   - Manual refresh button
   - Last updated timestamp

📊 Chart Selection for Dashboards:

TRENDS: Line charts
- Revenue over time
- User growth
- Performance metrics

COMPARISONS: Bar charts
- Sales by product
- Performance by region
- Before/after comparisons

COMPOSITION: Pie/Donut charts
- Market share
- Revenue breakdown
- Category distribution

DISTRIBUTION: Histograms
- Customer age distribution
- Response time distribution
- Order value distribution

RELATIONSHIPS: Scatter plots
- Price vs sales volume
- Customer value vs churn risk

GEOGRAPHIC: Maps
- Sales by region
- User locations
- Store performance

KPIs: Big numbers with sparklines
- Current value (large)
- Change vs previous (± %)
- Mini trend chart (sparkline)

🎨 DASHBOARD DESIGN BEST PRACTICES:

HIERARCHY:
1. Most important: KPIs (top)
2. Primary insights: Large charts (middle)
3. Details: Tables/small charts (bottom)

COLORS:
- Consistent color scheme (3-5 colors)
- Semantic colors (red=bad, green=good)
- Color-blind friendly
- Not too busy

SPACING:
- White space between elements
- Grouped related charts
- Clear sections

RESPONSIVENESS:
- Mobile-friendly (stacks vertically)
- Tablet-optimized
- Desktop full-featured

PERFORMANCE:
- Load data incrementally
- Cache when possible
- Show loading indicators
- Optimize queries

🔧 TECHNICAL IMPLEMENTATION:

STACK OPTIONS:

Option 1: Python + Plotly Dash
```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Analytics Dashboard"),
    dcc.Graph(id='revenue-chart'),
    dcc.Interval(id='interval', interval=60000)  # Refresh every 60s
])

@app.callback(
    Output('revenue-chart', 'figure'),
    Input('interval', 'n_intervals')
)
def update_chart(n):
    df = fetch_data()  # Get latest data
    fig = px.line(df, x='date', y='revenue')
    return fig

app.run_server()
```

Option 2: React + Chart.js
- FastAPI backend (data API)
- React frontend
- Chart.js for visualization
- Real-time via WebSockets

Option 3: Power BI / Tableau
- Business intelligence tools
- Drag-and-drop interface
- Enterprise features
- Higher cost

TOOLS AVAILABLE:
✓ {self.toolkit.create_dashboard_report.__name__} - Dashboard config
✓ {self.toolkit.visualization_recommendations.__name__} - Chart selection

📱 DASHBOARD TYPES:

EXECUTIVE DASHBOARD:
- High-level KPIs
- Strategic metrics
- Trend indicators
- Alert highlights
- Weekly/monthly refresh

OPERATIONAL DASHBOARD:
- Real-time data
- Detailed metrics
- Drill-down heavy
- Frequent refresh (minutes)
- Action-oriented

ANALYTICAL DASHBOARD:
- Complex analysis
- Multiple data sources
- Advanced filtering
- Export-friendly
- User exploration

COLLABORATION:
- Maya: Chart creation, data pipelines
- Alex: Backend API, data processing
- All analysts: KPI definitions, metric selection

DELIVERABLES:
- Live dashboard (URL)
- Dashboard screenshot (PDF)
- User guide (how to use)
- Data documentation
- Maintenance plan

Ready to create interactive dashboard! 📱
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "document_type": "Interactive Dashboard",
                "format": "HTML/Web",
                "features": ["Real-time", "Interactive", "Drill-down", "Export"],
                "technologies": ["Plotly Dash", "React + Chart.js", "Power BI/Tableau"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "dashboard_url.txt",
                "dashboard_screenshot.pdf",
                "user_guide.pdf",
                "dashboard_code.zip"
            ],
            next_steps="Define KPIs and data sources for dashboard"
        )
    
    def _quality_review(self, task: Task, context: list) -> TaskResult:
        """Quality review and proofreading"""
        
        thoughts = f"""
✅ QUALITY REVIEW - Lucas Rivera

Request: {task.title}

QUALITY ASSURANCE FRAMEWORK:

📋 COMPREHENSIVE REVIEW CHECKLIST:

1. CONTENT QUALITY:

   Accuracy:
   □ All facts verified
   □ Numbers double-checked
   □ Sources cited correctly
   □ Dates are accurate
   □ No unsupported claims

   Completeness:
   □ All required sections included
   □ All questions answered
   □ No missing context
   □ Appendices referenced
   □ All TODOs removed

   Logic & Flow:
   □ Logical progression
   □ Clear narrative arc
   □ Transitions smooth
   □ Conclusions supported by findings
   □ No contradictions

2. WRITING QUALITY:

   Grammar & Spelling:
   □ Spell check passed
   □ Grammar check passed
   □ Punctuation correct
   □ Capitalization consistent
   □ No typos

   Style & Tone:
   □ Consistent voice
   □ Appropriate for audience
   □ Professional tone
   □ Active voice (where appropriate)
   □ No jargon (or explained)

   Clarity:
   □ Sentences clear and concise
   □ Paragraphs focused
   □ No ambiguity
   □ Technical terms defined
   □ Acronyms spelled out (first use)

3. FORMAT & DESIGN:

   Layout:
   □ Consistent formatting
   □ Proper page breaks
   □ Headers/footers correct
   □ Page numbers sequential
   □ Margins consistent

   Typography:
   □ Font consistent
   □ Font sizes appropriate
   □ Hierarchy clear (H1, H2, H3)
   □ Bold/italic used correctly
   □ Readable (high contrast)

   Visual Elements:
   □ All figures numbered
   □ All tables numbered
   □ Captions present and descriptive
   □ High resolution (300 DPI)
   □ Proper alignment

4. STRUCTURE:

   Organization:
   □ Table of Contents accurate
   □ Page numbers match TOC
   □ Sections in logical order
   □ Headings descriptive
   □ Cross-references correct

   Executive Summary:
   □ Standalone (makes sense alone)
   □ All key points covered
   □ Concise (1-2 pages)
   □ Actionable
   □ Accurate (matches report)

   Citations:
   □ All sources cited
   □ Citation format consistent
   □ Links work (if digital)
   □ Bibliography complete
   □ No broken references

5. TECHNICAL ACCURACY:

   Data:
   □ Charts match data
   □ Calculations verified
   □ Units specified
   □ Percentages sum correctly
   □ Decimals appropriate

   Statistics:
   □ Test selection appropriate
   □ Assumptions validated
   □ P-values reported correctly
   □ Effect sizes included
   □ Confidence intervals stated

   Legal:
   □ Disclaimers present (if needed)
   □ Confidentiality marked
   □ No privileged info exposed
   □ Proper attribution
   □ Copyright respected

6. PROFESSIONAL POLISH:

   Branding:
   □ Company logo present
   □ Brand colors used
   □ Professional appearance
   □ Consistent with brand guidelines

   Metadata:
   □ Document title set
   □ Author information
   □ Creation date
   □ Version number
   □ Keywords (for searchability)

   Final Check:
   □ Prints correctly
   □ PDFs correctly
   □ File size reasonable
   □ All links work
   □ Compatible format

🔍 REVIEW METHODS:

1. SELF-REVIEW:
   - Read aloud (catches awkward phrasing)
   - Print and mark up (see differently)
   - Fresh eyes (come back next day)

2. PEER REVIEW:
   - Another team member reviews
   - Damian (Devil's Advocate) challenges
   - Technical expert verifies accuracy

3. STAKEHOLDER REVIEW:
   - Viktor (Orchestrator) strategic alignment
   - Client/Executive preview (if appropriate)

4. PROFESSIONAL EDIT:
   - Copy editing (grammar, style)
   - Substantive editing (structure, content)
   - Proofreading (final typos)

📝 COMMON ISSUES TO CATCH:

CONTENT:
- Inconsistent data between sections
- Missing context for readers
- Unsupported conclusions
- Contradictory statements

WRITING:
- Passive voice ("It was found" → "We found")
- Wordiness ("In order to" → "To")
- Redundancy ("Final conclusion" → "Conclusion")
- Clichés ("Think outside the box" → specific guidance)

FORMAT:
- Inconsistent heading styles
- Orphaned headers (heading at page bottom)
- Widows (single line at page top)
- Inconsistent spacing

TECHNICAL:
- Chart labels missing units
- Table numbers skip
- Figures not referenced in text
- Formulas incorrect

🛠️ REVIEW TOOLS:

Automated:
- Grammarly: Grammar and style
- Hemingway: Readability score
- Microsoft Word: Spell check, track changes
- PDF tools: Compression, accessibility check

Manual:
- Printed review copy
- Checklist (systematic)
- Multiple passes (focus on different aspects each time)

TOOLS AVAILABLE:
✓ {self.toolkit.report_quality_checklist.__name__} - Comprehensive QA checklist

DELIVERABLES:

1. Review Comments:
   - Marked-up document (track changes)
   - Comment summary
   - Priority issues highlighted

2. Corrected Version:
   - All issues fixed
   - Clean document (no track changes)
   - Ready for distribution

3. Quality Report:
   - Issues found and fixed
   - Quality score
   - Sign-off

COLLABORATION:
- ALL team members: Content accuracy review
- Damian: Challenge logic and conclusions
- Viktor: Strategic relevance check

Ready for quality review! ✅
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "review_type": "Quality Assurance",
                "checklist_areas": ["Content", "Writing", "Format", "Structure", "Technical", "Polish"],
                "methods": ["Self-review", "Peer review", "Stakeholder review", "Professional edit"],
                "deliverables": ["Review comments", "Corrected version", "Quality report"]
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=[
                "review_comments.docx",
                "corrected_document.pdf",
                "quality_report.pdf"
            ],
            next_steps="Provide document for quality review"
        )
    
    def _general_report_synthesis(self, task: Task, context: list) -> TaskResult:
        """General report synthesis support"""
        
        thoughts = f"""
📝 REPORT SYNTHESIS - Lucas Rivera

Request: {task.title}

REPORT GENERATION CAPABILITIES:

📚 Document Types:
- Executive Summaries (1-2 pages)
- Comprehensive Reports (15-50 pages)
- Presentations (10-15 slides)
- Interactive Dashboards (web-based)
- Quality Reviews (any document)

🎯 My Role:
I synthesize findings from the entire analytical team into
professional, actionable deliverables.

INPUT SOURCES:
✓ Elena (OSINT): Investigation findings, digital intelligence
✓ Marcus (Financial): Financial analysis, valuations, risk assessment
✓ Sofia (Market Research): Market trends, competitive intel, consumer insights
✓ Adrian (Legal): Legal research, compliance, contracts, risk
✓ Maya (Data Analyst): Statistical analysis, visualizations, models
✓ Alex (Technical): Document processing, data pipelines
✓ Viktor (Orchestrator): Strategic direction, priorities
✓ Damian (Devil's Advocate): Alternative perspectives, challenges

OUTPUT FORMATS:
📄 PDF: Professional, print-ready, locked
📝 DOCX: Editable source, track changes
📊 PPTX: Presentation slides
📱 HTML: Interactive dashboards, web reports
📊 Excel: Data tables, models

✍️ WRITING SPECIALIZATIONS:

1. EXECUTIVE COMMUNICATION:
   - C-level summaries
   - Board presentations
   - Investor reports
   - Strategic memos

2. ANALYTICAL REPORTS:
   - Investigation reports
   - Due diligence reports
   - Market research reports
   - Financial analysis reports

3. COMPLIANCE DOCUMENTATION:
   - Compliance reports
   - Audit findings
   - Risk assessments
   - Policy documents

4. BUSINESS INTELLIGENCE:
   - Dashboards
   - KPI reports
   - Performance analytics
   - Trend analysis

🔧 TOOLS AVAILABLE:
{chr(10).join([f'✓ {category}: {", ".join(tools[:2])}...' for category, tools in self.tools.items() if category not in ['status', 'supported_formats']])}

Supported Formats: {", ".join(self.toolkit.supported_formats)}

📊 QUALITY STANDARDS:

Professional:
✓ Consistent formatting
✓ Clear hierarchy
✓ Professional tone
✓ Brand-aligned design

Accurate:
✓ Facts verified
✓ Data checked
✓ Sources cited
✓ Calculations correct

Actionable:
✓ Clear recommendations
✓ Prioritized actions
✓ Assigned owners
✓ Defined timelines

Accessible:
✓ Clear language
✓ Defined jargon
✓ Visual aids
✓ Executive summary

🤝 COLLABORATION WORKFLOW:

1. INTAKE:
   - Viktor: Strategic brief
   - Team: Findings collection
   - Damian: Critical review

2. SYNTHESIS:
   - Identify key themes
   - Connect insights
   - Build narrative
   - Develop recommendations

3. DRAFTING:
   - Structure document
   - Write sections
   - Create visualizations
   - Integrate findings

4. REFINEMENT:
   - Team review
   - Stakeholder feedback
   - Quality assurance
   - Professional polish

5. DELIVERY:
   - Final document
   - Executive summary
   - Supporting materials
   - Presentation (if needed)

⏱️ TYPICAL TIMELINES:

Executive Summary: 1-2 days
Presentation: 2-3 days
Comprehensive Report: 2-3 weeks
Dashboard: 1-2 weeks (with development)
Quality Review: 1 day

🎯 DELIVERABLE EXAMPLES:

For Investigation:
- Executive Summary (2 pages)
- Full Report (30 pages)
- Presentation (12 slides)
- Evidence Appendix

For Market Research:
- Executive Summary (1 page)
- Market Report (20 pages)
- Presentation (15 slides)
- Dashboard (interactive)

For Due Diligence:
- Executive Summary (3 pages)
- DD Report (50 pages)
- Risk Register (Excel)
- Presentation (15 slides)

Ready to synthesize professional reports! 📝

PRIVACY NOTE:
All report generation done locally (LM Studio).
Sensitive client information never leaves your infrastructure.
"""
        
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={
                "capabilities": ["Executive summaries", "Reports", "Presentations", "Dashboards", "QA"],
                "formats": self.toolkit.supported_formats,
                "tools": self.tools,
                "privacy": "LOCAL (LM Studio)"
            },
            thoughts=thoughts.strip(),
            time_taken=0,
            artifacts=["report_capabilities_overview.pdf"],
            next_steps="Specify report type and provide team findings"
        )


# Quick test
if __name__ == "__main__":
    print("📝 Lucas Rivera - Report Synthesizer\n")
    
    agent = LucasAgent()
    
    print(f"Agent: {agent.name}")
    print(f"Role: {agent.role}")
    print(f"Specialization: {agent.specialization}")
    
    print(f"\nSupported Formats: {', '.join(agent.toolkit.supported_formats)}")
    
    print(f"\nTools Available:")
    for category, tools in agent.tools.items():
        if category not in ["status", "supported_formats"]:
            print(f"  {category}: {len(tools)} tools")
    
    print(f"\n{agent.tools.get('status', 'Ready!')}")
