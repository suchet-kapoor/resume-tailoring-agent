# Resume Tailoring Agent

## Agent Metadata
- **Name**: Resume Tailoring Agent
- **Version**: 1.0.0
- **Author**: Based on Uchenna Ejike's methodology
- **Description**: AI-powered resume tailoring agent that implements ATS-beating strategies
- **License**: MIT

## Agent Skills

### Core Skills
1. **Resume Analysis**
   - Parse PDF and DOCX resume files
   - Extract user experience, skills, and background
   - Identify transferable skills and achievements

2. **Job Description Processing**
   - Extract keywords and key phrases
   - Identify role requirements and qualifications
   - Analyze company values and culture mentions
   - Detect ATS system patterns

3. **Verbatim Keyword Matching**
   - Copy exact phrases from job descriptions
   - Avoid paraphrasing or synonym substitution
   - Maintain keyword density for ATS optimization

4. **Content Restructuring**
   - Mirror job description section headers
   - Reorganize experience to match role categories
   - Align content with target position structure

5. **ATS Optimization**
   - Format for single-column layout
   - Use standard fonts and formatting
   - Generate .docx output files
   - Ensure parsing compatibility

### Advanced Skills
6. **Role Title Alignment**
   - Match job titles to target positions
   - Maintain accuracy and authenticity
   - Adjust for different seniority levels

7. **Values Integration**
   - Create values alignment sections
   - Match company culture statements
   - Integrate mission-driven language

8. **Quantification Enhancement**
   - Suggest areas for metrics addition
   - Maintain achievement authenticity
   - Improve impact measurement

9. **Cover Letter Generation**
   - Apply 5-paragraph proven formula
   - Customize for specific companies
   - Integrate job-specific keywords

## Agent Capabilities

### Input Processing
- **Resume Formats**: PDF, DOCX, TXT
- **Job Description Sources**: Copy-paste text, formatted documents
- **Language Support**: English (primary)

### Output Generation
- **Resume Format**: ATS-optimized DOCX
- **Cover Letters**: Structured markdown/text
- **Keyword Reports**: Extracted terms and phrases
- **Optimization Suggestions**: Improvement recommendations

### Integration Points
- **AI Models**: Compatible with Claude, GPT, Copilot
- **File Systems**: Local storage and processing
- **Document Processing**: Python-docx, PyPDF2

## Tools and Dependencies

### Required Tools
1. **Document Processing**
   - `python-docx` - DOCX manipulation
   - `PyPDF2` - PDF text extraction
   - `openpyxl` - Excel file handling

2. **Text Analysis**
   - `spacy` - NLP processing
   - `nltk` - Text tokenization
   - `python-dateutil` - Date parsing

3. **Interface**
   - `streamlit` - Web interface (optional)
   - Standard file I/O operations

### AI Model Integration
- **Primary**: User's existing AI subscriptions
- **Context Files**: Complete documentation in `/docs`
- **Prompt Templates**: Structured in `/templates`

## Agent Workflow

### Phase 1: Setup (One-time)
1. User uploads base resume
2. Agent parses and stores user profile
3. Creates baseline content library

### Phase 2: Job Processing (Per Application)
1. User pastes job description
2. Agent extracts keywords and requirements
3. Identifies structural patterns

### Phase 3: Resume Tailoring
1. Applies verbatim keyword strategy
2. Restructures content to match job format
3. Integrates company values if present
4. Optimizes for target ATS system

### Phase 4: Output Generation
1. Generates tailored resume in DOCX format
2. Creates matching cover letter
3. Provides optimization report
4. Suggests quantification improvements

## Success Metrics

### Effectiveness Indicators
- **ATS Match Score**: Target 85%+ keyword alignment
- **Application Success**: Based on Uchenna's 6/week methodology
- **Time Efficiency**: <5 minutes per tailored resume
- **Format Compliance**: 100% ATS-compatible output

### Quality Assurance
- Maintains content accuracy
- Preserves user achievements
- Ensures professional presentation
- Validates technical requirements

## Usage Instructions

### For Developers
1. Clone repository
2. Install requirements: `pip install -r requirements.txt`
3. Read `/docs/agent-instructions.md` for complete AI context
4. Use with preferred AI model (Claude/GPT/Copilot)

### For End Users
1. Follow `/docs/user-guide.md`
2. Upload resume once for setup
3. Paste job descriptions for each application
4. Download tailored resume and cover letter

## Implementation Strategy

This agent is designed to work with **your existing AI subscriptions**:
- Complete context provided in documentation files
- No API keys or model hosting required
- Compatible with Claude, GPT, Copilot, and other LLMs
- Self-contained processing instructions

## References

Based on the proven methodology from:
**"How I Got 6 Interviews in One Week"** by Uchenna Ejike (January 2026)

Core principle: *"Your CV is not about you. It's about proving you match what they're looking for."*