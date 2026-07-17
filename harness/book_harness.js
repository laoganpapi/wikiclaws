export const meta = {
  name: 'book-harness',
  description: 'Per-system research, construction, and writing harness for the personality framework, with canon, citation, and red-team guards',
  whenToUse: 'Run with args {system, task, claims, focus}. system: s1|s2|s3|s4|all. task: research|develop|write|full. claims: array of claim strings to check (research/full). focus: free-text steer for the constructor/writer.',
  phases: [
    { title: 'Literature', detail: 'supporting case, contradicting case, citation verification, per system' },
    { title: 'Construct', detail: 'framework proposals reconciled with the evidence' },
    { title: 'Write', detail: 'chapter prose drafted to proposals/, never over live chapters' },
    { title: 'Guard', detail: 'canon keeper, red team, instrument impact' },
    { title: 'Synthesize', detail: 'editor-in-chief consolidates everything' },
  ],
}

const A = args || {}
const REPO = '/home/user/wikiclaws'
const SYSTEMS = {
  s1: { name: 'Social Energy Economy', doc: REPO + '/book/02_social_energy.md' },
  s2: { name: 'The Thinking Machine', doc: REPO + '/book/03_thinking_machine.md' },
  s3: { name: 'Emotional and Social Disposition', doc: REPO + '/book/04_emotional_social_disposition.md' },
  s4: { name: 'Objectives', doc: REPO + '/book/05_objectives.md' },
}
const chosen = (A.system && A.system !== 'all') ? [A.system] : ['s1', 's2', 's3', 's4']
const task = A.task || 'research'
const claims = Array.isArray(A.claims) ? A.claims : []
const focus = A.focus || ''

const CANON = `Read ${REPO}/book/00_architecture.md FIRST. Its axioms bind every output you produce:
preference not ability (three lanes: preference / capability / pathology — this framework is preference only);
self-understanding not prediction; neutral bipolar measures, no valence, no praise or deficit language
(collapse/degrade/volatile/spike are barred words); stated vs revealed are symmetric, the gap is the finding;
clean or silent (no shaky gap or slope is ever shown); snapshot not verdict; open text only where answering
is easy, structured choice wherever it reduces noise; de novo presentation with an internal novelty watch.
Also skim ${REPO}/book/metrics_catalog.md for the measures. `

const STYLE = `House style for any prose: declarative, precise, short sentences; define terms before use;
plain register a smart non-specialist reads easily; unsettled claims go under Open Questions, never stated
as settled; no valenced language about either pole of any measure. `

const LIT_SCHEMA = {
  type: 'object',
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          verdict: { type: 'string', enum: ['supported', 'partly-supported', 'contested', 'unsupported', 'unexamined-in-literature'] },
          evidence: { type: 'string', description: 'the named studies/traditions and what they actually show, 2-5 sentences' },
          citations: { type: 'array', items: { type: 'string' }, description: 'author-year strings for load-bearing sources' },
          requiredChange: { type: 'string', description: 'what the framework text must change if anything; empty if nothing' },
        },
        required: ['claim', 'verdict', 'evidence', 'citations', 'requiredChange'],
      },
    },
    noveltyNotes: { type: 'string', description: 'any construct here that risks relabeling an established one, for the novelty watch' },
  },
  required: ['verdicts', 'noveltyNotes'],
}

const CITE_SCHEMA = {
  type: 'object',
  properties: {
    checks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          citation: { type: 'string' },
          exists: { type: 'boolean' },
          saysWhatWeClaim: { type: 'string', enum: ['yes', 'stretched', 'no', 'could-not-verify'] },
          note: { type: 'string' },
        },
        required: ['citation', 'exists', 'saysWhatWeClaim', 'note'],
      },
    },
  },
  required: ['checks'],
}

const GUARD_SCHEMA = {
  type: 'object',
  properties: {
    violations: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          where: { type: 'string' },
          axiom: { type: 'string' },
          detail: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['where', 'axiom', 'detail', 'fix'],
      },
    },
    clean: { type: 'boolean' },
  },
  required: ['violations', 'clean'],
}

// ---- Phase 1-3: the four subgroups run as independent pipelines (no barrier between systems) ----
const packages = await pipeline(
  chosen,
  // Stage 1: literature subgroup — three checkers in parallel per system
  async (sys) => {
    const S = SYSTEMS[sys]
    const sysClaims = claims.length ? claims : ['Derive the 3-6 load-bearing empirical claims this chapter makes and check those.']
    const base = CANON + `Your system: ${S.name}. Read its chapter at ${S.doc}. Claims under examination:\n- ` + sysClaims.join('\n- ') + '\n\n'
    const [supporting, contradicting] = await parallel([
      () => agent(base + 'You are the SUPPORTING-CASE literature checker. Search the actual research literature (use web search) for the strongest evidence FOR each claim. Also serve as novelty watch: flag any construct that risks relabeling an established one. Report only what named sources actually show.', { label: `lit-support:${sys}`, phase: 'Literature', schema: LIT_SCHEMA }),
      () => agent(base + 'You are the CONTRADICTING-CASE literature checker. Search the actual research literature (use web search) for the strongest evidence AGAINST each claim, boundary conditions, and failed replications. Do not soften. Report only what named sources actually show.', { label: `lit-contra:${sys}`, phase: 'Literature', schema: LIT_SCHEMA }),
    ])
    const allCites = [...new Set([...(supporting ? supporting.verdicts.flatMap(v => v.citations) : []), ...(contradicting ? contradicting.verdicts.flatMap(v => v.citations) : [])])]
    const citecheck = allCites.length ? await agent(
      `You are the CITATION VERIFIER. For each citation below, verify with web search that the work exists (author, year, venue) and that it supports the use it was put to in this JSON evidence. "Stretched" means real paper, claim pushed past what it shows.\nCITATIONS: ${JSON.stringify(allCites)}\nEVIDENCE THEY SUPPORT: ${JSON.stringify({ supporting, contradicting })}`,
      { label: `cite-verify:${sys}`, phase: 'Literature', schema: CITE_SCHEMA }) : { checks: [] }
    return { sys, S, supporting, contradicting, citecheck }
  },
  // Stage 2: constructor (develop/full) — reconciles evidence into framework proposals
  async (pkg, sys) => {
    if (task === 'research') return { ...pkg, construction: null }
    pkg.construction = await agent(
      CANON + STYLE + `Your system: ${pkg.S.name} (${pkg.S.doc}). ${focus ? 'Author focus: ' + focus + '. ' : ''}You are the FRAMEWORK CONSTRUCTOR. Given the verified evidence below, propose how this system's constructs should change: keep / revise / add / retire, each with the evidence that motivates it and the axiom it must respect. Present options with a preliminary lean where a call is genuinely open; decide plainly where evidence is one-sided. Return markdown.\n\nEVIDENCE: ${JSON.stringify({ supporting: pkg.supporting, contradicting: pkg.contradicting, citecheck: pkg.citecheck })}`,
      { label: `construct:${sys}`, phase: 'Construct', effort: 'high' })
    return pkg
  },
  // Stage 3: writer (write/full) — drafts to proposals/, never touches live chapters
  async (pkg, sys) => {
    if (task !== 'write' && task !== 'full') return { ...pkg, proposalPath: null }
    const out = `${REPO}/book/proposals/${sys}_draft.md`
    await agent(
      CANON + STYLE + `Your system: ${pkg.S.name}. You are the WRITER. Using the current chapter (${pkg.S.doc})${pkg.construction ? ' and the constructor proposals below' : ''}, draft the revised chapter text. Write the complete draft to ${out} using the Write tool (create the proposals/ directory if needed). NEVER edit ${pkg.S.doc} itself — proposals only, the author decides what merges. Keep the chapter template: phenomenon, measures, decision rule, dynamic layer, illustrations, open questions. Return a 5-line summary of what changed and why.\n\n${pkg.construction ? 'CONSTRUCTOR PROPOSALS:\n' + pkg.construction : ''}`,
      { label: `write:${sys}`, phase: 'Write' })
    return { ...pkg, proposalPath: out }
  }
)

const done = packages.filter(Boolean)
log(`${done.length}/${chosen.length} system packages complete; guards next`)

// ---- Phase 4: global guards see ALL packages together (cross-system defects need the whole picture) ----
const guardInput = JSON.stringify(done.map(p => ({
  system: p.S.name,
  verdicts: { supporting: p.supporting, contradicting: p.contradicting, citecheck: p.citecheck },
  construction: p.construction, proposalPath: p.proposalPath,
})))
const [canon, redteam, impact] = await parallel([
  () => agent(CANON + `You are the CANON KEEPER. Check every package below (and any proposal files it names — read them) against the axioms, word bans, and cross-system boundaries (S2 cognitive sourcing vs S3 attention; reactivity moderation; three lanes). Report violations only.\n\nPACKAGES: ${guardInput}`, { label: 'guard:canon', phase: 'Guard', schema: GUARD_SCHEMA }),
  () => agent(CANON + `You are the RED TEAM. Attack the packages below as a hostile psychometrician and a hostile domain expert would: weakest evidence, circular constructs, claims outrunning citations, anything a real reviewer would land. Read any proposal files named. Report the hits that would actually land, as violations.\n\nPACKAGES: ${guardInput}`, { label: 'guard:redteam', phase: 'Guard', schema: GUARD_SCHEMA }),
  () => agent(CANON + `You are the INSTRUMENT IMPACT ASSESSOR. For each proposed framework change in the packages below, name exactly what must change in ${REPO}/book/metrics_catalog.md, ${REPO}/book/instrument_design.md, and the app at ${REPO}/app/v2.html so book and test stay consistent. Read those files. Report each needed change as a violation entry (where=file, axiom=consistency, detail=what is now inconsistent, fix=the change).\n\nPACKAGES: ${guardInput}`, { label: 'guard:impact', phase: 'Guard', schema: GUARD_SCHEMA }),
])

// ---- Phase 5: editor-in-chief ----
const memo = await agent(
  STYLE + `You are the EDITOR-IN-CHIEF. Consolidate the harness run into one markdown memo for the authors: 1) per system, the claim verdicts with citations (flag any citation the verifier marked stretched/no/could-not-verify); 2) the construction proposals worth the authors' attention (options and leans, compressed); 3) guard findings (canon, red team, instrument impact), deduplicated, ordered by consequence; 4) proposal files written, if any, and what awaits author decision. Plain English. Return ONLY the markdown.\n\nPACKAGES: ${guardInput}\nGUARDS: ${JSON.stringify({ canon, redteam, impact })}`,
  { label: 'editor-in-chief', phase: 'Synthesize', effort: 'high' })

return {
  systems: done.map(p => p.S.name),
  task,
  proposals: done.map(p => p.proposalPath).filter(Boolean),
  guardViolations: [canon, redteam, impact].filter(Boolean).reduce((n, g) => n + g.violations.length, 0),
  memo,
}
