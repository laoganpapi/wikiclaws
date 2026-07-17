export const meta = {
  name: 'book-harness',
  description: 'Per-system research, construction, and writing harness for the personality framework, with canon, citation, and red-team guards',
  whenToUse: 'Run with args {system, task, claims, focus}. system: s1|s2|s3|s4|all. task: research|develop|write|full. claims: array of claim strings to check (research/full). focus: free-text steer for the constructor/writer.',
  phases: [
    { title: 'Literature', detail: 'claim scan, supporting and contradicting checks in small batches, citation verification' },
    { title: 'Construct', detail: 'framework proposals reconciled with the evidence, written to proposals/' },
    { title: 'Write', detail: 'chapter prose drafted to proposals/, never over live chapters' },
    { title: 'Guard', detail: 'canon keeper and red team per system, cross-system pass, per-artifact instrument impact' },
    { title: 'Synthesize', detail: 'editor-in-chief consolidates the digests' },
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

// ---- Context discipline helpers ----
// Every agent gets ONE bounded job. Anything inlined into a prompt is capped; anything long lives
// in a file the agent reads itself. These two helpers enforce that everywhere.
const cap = (s, n) => {
  const t = typeof s === 'string' ? s : (s == null ? '' : JSON.stringify(s))
  return t.length > n ? t.slice(0, n) + ' ...[truncated]' : t
}
const chunk = (arr, n) => {
  const out = []
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n))
  return out
}
const CLAIMS_PER_CHECKER = 3   // a literature checker examines at most this many claims
const CITES_PER_VERIFIER = 8   // a citation verifier examines at most this many citations

const CANON = `Read ${REPO}/book/00_architecture.md FIRST. Its axioms bind every output you produce:
preference not ability (three lanes: preference / capability / pathology — this framework is preference only);
self-understanding not prediction; neutral bipolar measures, no valence, no praise or deficit language
(collapse/degrade/volatile/spike are barred words); stated vs revealed are symmetric, the gap is the finding;
clean or silent (no shaky gap or slope is ever shown); snapshot not verdict; open text only where answering
is easy, structured choice wherever it reduces noise; de novo presentation with an internal novelty watch. `

const STYLE = `House style for any prose: declarative, precise, short sentences; define terms before use;
plain register a smart non-specialist reads easily; unsettled claims go under Open Questions, never stated
as settled; no valenced language about either pole of any measure. `

const CLAIMS_SCHEMA = {
  type: 'object',
  properties: {
    claims: { type: 'array', items: { type: 'string' }, description: 'the 3-6 load-bearing empirical claims, each one self-contained sentence' },
  },
  required: ['claims'],
}

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
  },
  required: ['verdicts'],
}

const NOVELTY_SCHEMA = {
  type: 'object',
  properties: {
    noveltyNotes: { type: 'string', description: 'constructs that risk relabeling an established one, with the established name; empty string if none' },
  },
  required: ['noveltyNotes'],
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

// ---- Phases 1-4a: the four subgroups run as independent pipelines (no barrier between systems) ----
const packages = await pipeline(
  chosen,
  // Stage 1: literature subgroup.
  // Subdivided so no single agent both derives claims and checks them, and no checker holds more
  // than CLAIMS_PER_CHECKER claims: claim scanner -> batched supporting/contradicting checkers
  // (+ one dedicated novelty watcher) -> batched citation verifiers fed citation->use pairs only.
  async (sys) => {
    const S = SYSTEMS[sys]
    let sysClaims = claims
    if (!sysClaims.length) {
      const scanned = await agent(
        CANON + `Your system: ${S.name}. You are the CLAIM SCANNER. Read the chapter at ${S.doc} and extract the 3-6 load-bearing empirical claims it makes — the ones the framework fails without. Each claim one self-contained sentence, checkable against research literature. Do NOT check them; extraction only.`,
        { label: `claims:${sys}`, phase: 'Literature', schema: CLAIMS_SCHEMA, effort: 'low' })
      sysClaims = scanned ? scanned.claims : []
    }
    if (!sysClaims.length) { log(`${sys}: no claims to check, package dropped`); return null }

    const batches = chunk(sysClaims, CLAIMS_PER_CHECKER)
    const checkerBase = (batch) => CANON + `Your system: ${S.name}. Chapter for context: ${S.doc} (read it, but examine ONLY the claims listed here, not the whole chapter):\n- ` + batch.join('\n- ') + '\n\n'
    const litThunks = []
    for (let i = 0; i < batches.length; i++) {
      const b = batches[i]
      litThunks.push(() => agent(checkerBase(b) + 'You are the SUPPORTING-CASE literature checker. Search the actual research literature (use web search) for the strongest evidence FOR each claim above. Report only what named sources actually show.', { label: `lit-support:${sys}:b${i + 1}`, phase: 'Literature', schema: LIT_SCHEMA }))
    }
    for (let i = 0; i < batches.length; i++) {
      const b = batches[i]
      litThunks.push(() => agent(checkerBase(b) + 'You are the CONTRADICTING-CASE literature checker. Search the actual research literature (use web search) for the strongest evidence AGAINST each claim above, boundary conditions, and failed replications. Do not soften. Report only what named sources actually show.', { label: `lit-contra:${sys}:b${i + 1}`, phase: 'Literature', schema: LIT_SCHEMA }))
    }
    litThunks.push(() => agent(
      CANON + `Your system: ${S.name}. You are the NOVELTY WATCHER. Read the chapter at ${S.doc} and, with web search, flag any construct in it that risks relabeling an established construct in the literature (name the established construct and tradition). This is your ONLY job; do not evaluate the claims.`,
      { label: `novelty:${sys}`, phase: 'Literature', schema: NOVELTY_SCHEMA }))
    const litResults = await parallel(litThunks)
    const nB = batches.length
    const supporting = litResults.slice(0, nB).filter(Boolean).flatMap(r => r.verdicts)
    const contradicting = litResults.slice(nB, 2 * nB).filter(Boolean).flatMap(r => r.verdicts)
    const noveltyNotes = litResults[2 * nB] ? litResults[2 * nB].noveltyNotes : ''

    // Citation verifiers get citation -> claimed-use pairs, never the full verdict JSON.
    const useMap = {}
    for (const v of [...supporting, ...contradicting]) {
      for (const c of (v.citations || [])) {
        if (!useMap[c]) useMap[c] = []
        if (useMap[c].length < 2) useMap[c].push({ claim: cap(v.claim, 160), verdict: v.verdict, evidenceExcerpt: cap(v.evidence, 280) })
      }
    }
    const citePairs = Object.keys(useMap).map(c => ({ citation: c, usedFor: useMap[c] }))
    const citeResults = await parallel(chunk(citePairs, CITES_PER_VERIFIER).map((batch, i) => () => agent(
      `You are the CITATION VERIFIER. For each citation below, verify with web search that the work exists (author, year, venue) and that it supports the use recorded next to it. "Stretched" means real paper, claim pushed past what it shows. Verify ONLY these pairs.\nPAIRS: ${JSON.stringify(batch)}`,
      { label: `cite-verify:${sys}:b${i + 1}`, phase: 'Literature', schema: CITE_SCHEMA })))
    const citecheck = { checks: citeResults.filter(Boolean).flatMap(r => r.checks) }

    // The digest is the ONLY form of this evidence that downstream prompts ever inline.
    const digest = {
      system: S.name,
      supporting: supporting.map(v => ({ claim: cap(v.claim, 200), verdict: v.verdict, evidence: cap(v.evidence, 400), requiredChange: cap(v.requiredChange, 300) })),
      contradicting: contradicting.map(v => ({ claim: cap(v.claim, 200), verdict: v.verdict, evidence: cap(v.evidence, 400), requiredChange: cap(v.requiredChange, 300) })),
      citationFlags: citecheck.checks.filter(k => !k.exists || k.saysWhatWeClaim !== 'yes').map(k => ({ citation: k.citation, exists: k.exists, saysWhatWeClaim: k.saysWhatWeClaim, note: cap(k.note, 200) })),
      noveltyNotes: cap(noveltyNotes, 800),
    }
    return { sys, S, supporting, contradicting, citecheck, digest }
  },
  // Stage 2: constructor (develop/full). Reads the digest, writes its FULL proposal to a file,
  // returns only a short summary — so no later prompt ever inlines constructor long-form output.
  async (pkg, sys) => {
    if (task === 'research') return { ...pkg, constructionSummary: null, constructionPath: null }
    const out = `${REPO}/book/proposals/${sys}_construction.md`
    const summary = await agent(
      CANON + STYLE + `Your system: ${pkg.S.name} (chapter at ${pkg.S.doc} — read it). ${focus ? 'Author focus: ' + focus + '. ' : ''}You are the FRAMEWORK CONSTRUCTOR. Given the verified evidence digest below, propose how this system's constructs should change: keep / revise / add / retire, each with the evidence that motivates it and the axiom it must respect. Present options with a preliminary lean where a call is genuinely open; decide plainly where evidence is one-sided. Write the FULL proposal as markdown to ${out} using the Write tool (create the directory if needed). Return ONLY a summary of at most 15 lines.\n\nEVIDENCE DIGEST: ${JSON.stringify(pkg.digest)}`,
      { label: `construct:${sys}`, phase: 'Construct', effort: 'high' })
    return { ...pkg, constructionSummary: cap(summary, 2000), constructionPath: out }
  },
  // Stage 3: writer (write/full). Gets file PATHS (chapter + construction proposal), reads them
  // itself, drafts to proposals/, never touches live chapters.
  async (pkg, sys) => {
    if (task !== 'write' && task !== 'full') return { ...pkg, proposalPath: null }
    const out = `${REPO}/book/proposals/${sys}_draft.md`
    await agent(
      CANON + STYLE + `Your system: ${pkg.S.name}. You are the WRITER. Read the current chapter at ${pkg.S.doc}${pkg.constructionPath ? ' and the constructor proposal at ' + pkg.constructionPath : ''}, then draft the revised chapter text. Write the complete draft to ${out} using the Write tool (create the directory if needed). NEVER edit ${pkg.S.doc} itself — proposals only, the author decides what merges. Keep the chapter template: phenomenon, measures, decision rule, dynamic layer, illustrations, open questions. Return a 5-line summary of what changed and why.`,
      { label: `write:${sys}`, phase: 'Write' })
    return { ...pkg, proposalPath: out }
  },
  // Stage 4a: per-system guards. Each canon keeper / red team pair sees ONE system's digest plus
  // the file paths of that system's outputs (read on demand), never all packages at once.
  async (pkg, sys) => {
    const files = [pkg.constructionPath, pkg.proposalPath].filter(Boolean)
    const fileNote = files.length ? `Also read and check these output files: ${files.join(', ')}. ` : ''
    const guardBase = CANON + `Scope: ONLY the system "${pkg.S.name}" (chapter at ${pkg.S.doc}). ${fileNote}`
    const [canon, redteam] = await parallel([
      () => agent(guardBase + `You are the CANON KEEPER. Check this system's evidence digest and output files against the axioms and word bans. Report violations only.\n\nDIGEST: ${JSON.stringify(pkg.digest)}`, { label: `guard-canon:${sys}`, phase: 'Guard', schema: GUARD_SCHEMA }),
      () => agent(guardBase + `You are the RED TEAM. Attack this system's evidence digest and output files as a hostile psychometrician and a hostile domain expert would: weakest evidence, circular constructs, claims outrunning citations, anything a real reviewer would land. Report the hits that would actually land, as violations.\n\nDIGEST: ${JSON.stringify(pkg.digest)}`, { label: `guard-redteam:${sys}`, phase: 'Guard', schema: GUARD_SCHEMA }),
    ])
    return { ...pkg, canon: canon || { violations: [], clean: true }, redteam: redteam || { violations: [], clean: true } }
  }
)

const done = packages.filter(Boolean)
log(`${done.length}/${chosen.length} system packages complete; cross-system guards next`)

// ---- Phase 4b: cross-system guards (barrier — these genuinely need every package) ----
// Inputs stay bounded: digests only, never constructor/writer long-form output.
const allDigests = done.map(p => p.digest)

// Cross-system canon pass: only boundaries between systems, only when more than one system ran.
const crossCanon = done.length > 1 ? await agent(
  CANON + `You are the CROSS-SYSTEM CANON KEEPER. Per-system checks are already done — do NOT repeat them. Check ONLY defects that span systems: boundary bleed (S2 cognitive sourcing vs S3 attention; S3 reactivity as moderator of S2 stake-slopes), one construct measured twice under two names, contradictory required changes between systems, and any cross-system claim the digests below jointly break.\n\nDIGESTS: ${JSON.stringify(allDigests)}`,
  { label: 'guard-cross', phase: 'Guard', schema: GUARD_SCHEMA }) : { violations: [], clean: true }

// Instrument impact: one agent PER ARTIFACT (catalog / design doc / app), each reading only its
// own file and receiving only the compressed change list — never all three files in one context.
const changeList = done.flatMap(p => [
  ...[...p.digest.supporting, ...p.digest.contradicting].filter(v => v.requiredChange).map(v => ({ system: p.S.name, claim: v.claim, change: v.requiredChange })),
  ...(p.constructionSummary ? [{ system: p.S.name, claim: 'constructor proposal (full text at ' + p.constructionPath + ')', change: p.constructionSummary }] : []),
])
const ARTIFACTS = [
  { key: 'catalog', file: REPO + '/book/metrics_catalog.md', desc: 'the metrics catalog' },
  { key: 'design', file: REPO + '/book/instrument_design.md', desc: 'the instrument design document' },
  { key: 'app', file: REPO + '/app/v2.html', desc: 'the live assessment app (large file: search it with Grep for affected metrics/screens rather than reading it end to end)' },
]
const impacts = changeList.length ? await parallel(ARTIFACTS.map(a => () => agent(
  CANON + `You are the INSTRUMENT IMPACT ASSESSOR for ${a.desc} at ${a.file}. For each proposed framework change below, name exactly what must change in THIS artifact (and nothing else) so book and test stay consistent. Read the artifact. Report each needed change as a violation entry (where=location in the file, axiom=consistency, detail=what is now inconsistent, fix=the change). If a change does not touch this artifact, skip it.\n\nPROPOSED CHANGES: ${JSON.stringify(changeList)}`,
  { label: `guard-impact:${a.key}`, phase: 'Guard', schema: GUARD_SCHEMA }))) : []
const impact = { violations: impacts.filter(Boolean).flatMap(g => g.violations), clean: impacts.filter(Boolean).every(g => g.clean) }

// ---- Phase 5: editor-in-chief. Consolidates DIGESTS and guard verdicts, reading proposal files
// on demand — never fed raw packages or full guard transcripts. ----
const editorInput = done.map(p => ({
  system: p.S.name,
  digest: p.digest,
  constructionSummary: p.constructionSummary,
  constructionPath: p.constructionPath,
  proposalPath: p.proposalPath,
  guards: { canon: p.canon.violations, redteam: p.redteam.violations },
}))
const memo = await agent(
  STYLE + `You are the EDITOR-IN-CHIEF. Consolidate the harness run into one markdown memo for the authors: 1) per system, the claim verdicts with any flagged citations; 2) the construction proposals worth the authors' attention (read the constructionPath files for detail where the summary is thin); 3) guard findings (per-system canon and red team, cross-system, instrument impact), deduplicated, ordered by consequence; 4) proposal files written, if any, and what awaits author decision. Plain English. Return ONLY the markdown.\n\nSYSTEMS: ${JSON.stringify(editorInput)}\nCROSS-SYSTEM: ${JSON.stringify(crossCanon.violations)}\nINSTRUMENT IMPACT: ${JSON.stringify(impact.violations)}`,
  { label: 'editor-in-chief', phase: 'Synthesize', effort: 'high' })

const guardViolations = done.reduce((n, p) => n + p.canon.violations.length + p.redteam.violations.length, 0)
  + crossCanon.violations.length + impact.violations.length

return {
  systems: done.map(p => p.S.name),
  task,
  proposals: done.flatMap(p => [p.constructionPath, p.proposalPath]).filter(Boolean),
  guardViolations,
  memo,
}
