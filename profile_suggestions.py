"""Conservative, local form suggestions; never verified facts or model extraction."""
import re
from datetime import date


def suggest_profile(package):
    candidates={}
    def add(field,value,page,line):
        candidates.setdefault(field,{}).setdefault(value,[]).append(dict(source=page['ref'],quote=line))
    for source in package['sources']:
        for page in source['pages']:
            for line in page['text'].splitlines():
                borrower=re.search(r'^Borrower(?: and legal entity)?\s*:\s*(.+)$',line,re.I)
                if borrower:add('borrower',borrower[1].strip(),page,line)
                for pattern,field in ((r'(?:proposed transaction date|pro forma at|transaction as of)\s*:?\s*(\d{4}-\d{2}-\d{2})','transaction_date'),(r'(?:review as of|review date)\s*:?\s*(\d{4}-\d{2}-\d{2})','review_as_of')):
                    for match in re.finditer(pattern,line,re.I):
                        try:date.fromisoformat(match[1])
                        except ValueError:continue
                        add(field,match[1],page,line)
                span=re.search(r'Annual projection:\s*(\d{4}-\d{2}-\d{2})\s+through\s+(\d{4}-\d{2}-\d{2})',line,re.I)
                if span:
                    try:start,end=date.fromisoformat(span[1]),date.fromisoformat(span[2])
                    except ValueError:continue
                    if start<end:
                        add('annual_start',span[1],page,line);add('annual_end',span[2],page,line)
                        add('annual_kind','SUPPLIED_ANNUAL_PROJECTION',page,line)
            # Only infer calendar boundaries where this page explicitly defines them.
            if re.search(r'Calendar years:\s*01 January through 31 December',page['text'],re.I):
                for line in page['text'].splitlines():
                    match=re.search(r'(\d{4}) and (\d{4}) columns.*supplied annual projections',line,re.I)
                    if match and int(match[1])<int(match[2]):
                        add('previous_start',match[1]+'-01-01',page,line)
                        add('previous_end',match[1]+'-12-31',page,line)
                        add('annual_start',match[2]+'-01-01',page,line)
                        add('annual_end',match[2]+'-12-31',page,line)
                        add('annual_kind','SUPPLIED_ANNUAL_PROJECTION',page,line)
    values={field:next(iter(options)) for field,options in candidates.items() if len(options)==1}
    evidence={field:options[values[field]] for field,options in candidates.items() if field in values}
    # Review date is a user-selected analysis date, not the document preparation date.
    if 'review_as_of' not in values and 'review_as_of' not in candidates:
        try:values['review_as_of']=date.fromisoformat(package['observed_at_utc'][:10]).isoformat()
        except (ValueError,KeyError):pass
    return dict(values=values,evidence=evidence,conflicts=[f for f,v in candidates.items() if len(v)>1])
