# Red Team 13 Memo: Citation Accuracy Review

*Reviewer: Citation-accuracy red team (law-review/ICJ-clerk/Lancet-editor/Standards-desk posture). Round 1. As of 25 May 2026.*

## 1. Executive Summary

Scope of review: the synthesis (`09_synthesis_output.md`, 288 lines) and the executive brief (`10_executive_brief_output.md`, 81 lines). Cross-checks against the eight upstream outputs were used as a triangulation step. Verification against primary sources was attempted via WebFetch and WebSearch.

A significant operational constraint: WebFetch returned HTTP 403 on every primary-source attempt against icj-cij.org, icc-cpi.int, ohchr.org, who.int, un.org (unispal), un.org (icc-cpi), icty.org, irmct.org, hrlibrary.umn.edu, ipcinfo.org, refworld.org, ejiltalk.org, lawfaremedia.org, diakonia.se, en.wikipedia.org, jpost.com, timesofisrael.com, and lancet.com. Verification therefore relied on WebSearch result digests, which return curated excerpts from the same primary sources. Where the digest reproduced the primary quotation, paragraph number, or figure, that is treated as verified. Where the digest did not reproduce the underlying text, the citation is recorded as a retrieval gap.

Total citations and assertions tested: 78 (key items across quotations, paragraph numbers, dates, names, document IDs, figures). Errors found:

- HIGH severity: 1
- MEDIUM severity: 6
- LOW severity: 9
- Retrieval gaps: 11
- Whitelist violations: 2 (both also flagged under MEDIUM)

Top-line readiness assessment: the citation work is largely defensible. The Gallant statement, the ICJ ¶54 plausibility quote, the ICC charging language (with one MEDIUM caveat), the IPC 22 August 2025 finding, the UN CoI A/HRC/60/CRP.3 attribution, the Amnesty MDE 15/8668/2024 attribution, the Spagat *Lancet Global Health* figures (75,200; 95% CI 63,600–86,800; 56.2%; 49,090 MoH; 34.7% gap), and the *Croatia* ¶148 / *Bosnia* ¶373 / *Bosnia* ¶209 controlling formulations all verified against searched primaries. The defects below are correctable without restructuring the synthesis; the single HIGH item is a paraphrase-as-quotation problem in the Hamas Charter passage that requires either re-quoting verbatim or restyling as paraphrase.

## 2. HIGH-severity findings

### H1. Hamas 1988 Charter, Article 7: paraphrase presented as direct quotation, attributed to Yale Avalon Project translation

**Where:** Synthesis §5(e), line 206. Text reads:
> "The Day of Judgement will not come about until Muslims fight the Jews, when the Jew will hide behind stones and trees. The stones and trees will say: 'O Muslims, O Abdullah, there is a Jew behind me, come and kill him.' Except the *Gharqad* tree, which is the tree of the Jews" (Yale Avalon Project translation).

**Primary text (Yale Avalon Project translation of the 1988 Hamas Covenant, Article 7):**
> "The Day of Judgement will not come about until Moslems fight the Jews (killing the Jews), when the Jew will hide behind stones and trees. The stones and trees will say O Moslems, O Abdulla, there is a Jew behind me, come and kill him. Only the Gharkad tree, (evidently a certain kind of tree) would not do that because it is one of the trees of the Jews."

**Findings:**
- Synthesis renders "Moslems" as "Muslims" silently. The Avalon translation is historical; the spelling shift is a paraphrase, not a quotation.
- Synthesis drops the parenthetical "(killing the Jews)" without ellipsis.
- Synthesis renders "Abdulla" as "Abdullah" silently.
- Synthesis renders "Gharkad" as "Gharqad" and italicises it (Avalon does neither).
- The final clause is rewritten: Avalon's "Only the Gharkad tree, (evidently a certain kind of tree) would not do that because it is one of the trees of the Jews" becomes "Except the *Gharqad* tree, which is the tree of the Jews." This is reformulation, not transcription.

**Why HIGH:** The passage is presented inside quotation marks with attribution to a named translation. Five separate textual changes from that named translation. An adversary using this passage to attack the report's accuracy can demonstrate that the quoted text does not match the cited source. Recommended remediation: replace with the verbatim Avalon text inside quotation marks, or drop the quotation marks and present as paraphrase with citation to Avalon. Cross-doc note: this passage appears only in the synthesis; the executive brief does not reproduce it.

## 3. MEDIUM-severity findings

### M1. ICC arrest-warrant charges quoted with a charge dropped from the main string

**Where:** Synthesis §3, line 60 quotes the ICC charges as:
> "the war crime of starvation as a method of warfare; and the crimes against humanity of murder, persecution, and other inhumane acts"

and then separately quotes:
> "reasonable grounds to believe that Mr Netanyahu and Mr Gallant bear criminal responsibility as civilian superiors for the war crime of intentionally directing an attack against the civilian population."

Executive brief §3, line 23, reproduces only the first formulation.

**Primary text (ICC press release, 21 November 2024, as reproduced across UN News, ICC-CPI press release excerpts, and Amnesty/secondary summaries):** The Chamber found "reasonable grounds to believe that Mr Netanyahu and Mr Gallant each bear criminal responsibility as civilian superiors for the war crime of intentionally directing an attack against the civilian population … the war crime of starvation as a method of warfare … and the crimes against humanity of murder, persecution, and other inhumane acts."

**Finding:** The synthesis's first quotation excises "the war crime of intentionally directing an attack against the civilian population" from a list in which the press release groups it with the other charges, then presents that charge in a second quotation as a "further" finding. This understates the charges in the main quoted string and creates the impression that "intentionally directing an attack against the civilian population" was a separate, ancillary finding rather than co-equal with the other charges. The executive brief drops it entirely.

**Severity:** MEDIUM. The cited language is real ICC language; the issue is that the most-quoted formulation in the synthesis is sub-set rather than the full list. Recommended remediation: replace the synthesis §3 quoted list with a single quotation containing all three war-crime/CAH heads. Correct the executive brief §3 to add "intentionally directing an attack against the civilian population."

### M2. Hamas Charter "(2017)" reference to "Article 16" quote source unclear

**Where:** Synthesis §5(e), line 206: "The 2017 *Document of General Principles and Policies*, Article 16, states: 'Hamas affirms that its conflict is with the Zionist project not with the Jews because of their religion. Hamas does not wage a struggle against the Jews because they are Jewish but wages a struggle against the Zionists who occupy Palestine' (Hamas, 1 May 2017)."

**Finding:** The widely-used numbering of the 2017 Document varies across translations; the substantive anti-Jewish disclaimer is most commonly cited as paragraphs 16–17 or, depending on translation, as numbered articles. The synthesis does not specify which translation it is using. Retrieval of an authoritative English-language Hamas-published version was not possible within this review (WebFetch 403). MEDIUM because the quote is widely circulated and broadly accurate as paraphrase; but a single named source for the translation should be cited (e.g., the Middle East Forum English-language version, or a peer-reviewed citation). Recommended remediation: name the translation and verify article number.

### M3. UN CoI quote attributed to A/HRC/60/CRP.3 but sourced via OHCHR press release

**Where:** Synthesis §5(b), line 178: "The UN CoI concluded: 'Israel is responsible for the commission of genocide in Gaza. It is clear that there is an intent to destroy the Palestinians in Gaza through acts that meet the criteria set forth in the Genocide Convention' (OHCHR press release, 16 September 2025, summarising A/HRC/60/CRP.3)."

**Finding:** The quotation appears to be drawn from the OHCHR press release rather than the body of A/HRC/60/CRP.3 itself. The press release is itself a primary OHCHR document, so attribution is defensible; but the citation reads "summarising A/HRC/60/CRP.3" without confirming that the quoted sentence appears verbatim in the report. WebFetch to the OHCHR PDF returned 403. Recommended remediation: confirm the quoted text appears verbatim in CRP.3 (or attribute solely to the press release). Synthesis §6, line 226, repeats the second sentence ("It is clear that there is an intent to destroy ...") attributed to "Pillay's accompanying statement," which is consistent with a press-release/statement origin rather than the report body itself.

### M4. UNFPA "Situation Report, May/June 2025" date-citation mismatch with reported figure

**Where:** Synthesis §4(d), line 130 and executive brief §4(d), line 41: "UNFPA reported approximately 17,000 births in Gaza in the first six months of 2025, a 41% drop relative to the same period in 2022, with over 2,600 miscarriages and 220 pregnancy-related deaths before delivery (UNFPA Situation Report, May/June 2025)."

**Finding:** The 17,000-births/41%-drop figure was released in UNFPA's late-July 2025 press release ("UNFPA warns of catastrophic birth outcomes in Gaza") and reflects the *first half of 2025*, which by definition includes data through end-June. The UNFPA "Situation Report" for May–June 2025 is a distinct document; whether it contains the same 17,000 / 41% / 2,600 figures has not been verified (WebFetch 403). The figure may be from the July 23 2025 UNFPA news release rather than the May/June situation report. Recommended remediation: replace citation with UNFPA news release of 23 July 2025, or confirm the figures appear in the named situation report.

### M5. Khatib/McKee/Yusuf framing as "an order-of-magnitude estimate"

**Where:** Synthesis §4(a), line 78: "the *Lancet* correspondence by Khatib, McKee, and Yusuf (5 July 2024) suggested, applying a 4:1 indirect-to-direct ratio to the then-current 37,396 direct deaths, that total conflict-attributable mortality could reach 186,000; the authors framed this as an order-of-magnitude estimate."

**Finding:** The Lancet correspondence (which is not peer-reviewed; the Lancet labels correspondence as "reflections from readers") frames the 186,000 number with the words "not implausible" and describes it as an extrapolation, not specifically as an "order-of-magnitude estimate." Synthesis's "order-of-magnitude" framing is a defensible characterisation but is not a direct quotation; the synthesis does not place it in quotation marks, so this is a soft attribution issue rather than a misquotation. The synthesis also does not flag the correspondence's non-peer-reviewed status, which is methodologically relevant. Recommended remediation: note "not peer-reviewed correspondence" inline.

### M6. Whitelist compliance: Haaretz and CNN as primary citations for January 2026 IDF estimate

**Where:** Synthesis §1, line 15, and §4(a), line 80: "An internal Israeli military estimate reported in January 2026 of 'about 70,000 Gazans killed' is, on the public record, the first reported concurrence at the order of magnitude (Haaretz, 29 January 2026; CNN, 30 January 2026)." Executive brief §4(a), line 29, repeats Haaretz citation.

**Finding:** The plan whitelist (`00_plan.md` §"Sourcing whitelist") names ICJ/ICC filings, UN bodies, ICRC, named human-rights organisations, peer-reviewed journals, Israeli government official statements / IDF Spokesperson channels, Hamas official statements, and named scholars. Haaretz and CNN are not on the whitelist. The IDF Spokesperson is on the whitelist and is quoted in the synthesis as having said the figure "does not reflect official IDF data," which is on-whitelist. But the primary attribution for the 70,000 figure runs through Haaretz/Yedioth Ahronoth/CNN reporting of unnamed Israeli officials, not through any whitelisted Israeli government channel. The synthesis's footnote that the IDF Spokesperson "did not dispute it" is the closest the figure comes to whitelisted attribution. This is a structural whitelist exception that should be flagged inline, not silently sourced through non-whitelisted outlets.

**Severity:** MEDIUM, dual-flagged as whitelist violation (Whitelist 1 of 2 in §7 below).

## 4. LOW-severity findings

### L1. ICJ Order of 26 January 2024, vote breakdown on measure (vi)

**Where:** Synthesis §3, line 54: "Measures (i), (ii), (v), and (vi) passed 15 to 2 (Sebutinde and ad hoc Judge Barak dissenting); measures (iii) and (iv) passed 16 to 1, with Barak voting in favour."

**Finding:** Upstream agent 2 output (line 28) lists measures (i), (ii), (v), (vi) as all 15-2 with Sebutinde and Barak against; (iii) and (iv) as 16-1 with Sebutinde against only. Search-verified for measures (iii), (iv), (v) and the reporting requirement (vi). Recommended remediation: none; consistent with upstream and with searched secondary summaries.

### L2. Genocide Convention entry-into-force citation conflates dates

**Where:** Synthesis §2, line 27: "The Genocide Convention entered into force on 12 January 1951 (UN GA Res. 260 A (III))."

**Finding:** GA Res. 260 A (III) was adopted 9 December 1948 (the adoption resolution). Entry into force was 12 January 1951 by operation of Article XIII after the twentieth instrument of ratification. The synthesis's parenthetical attaches the resolution to the entry-into-force date in a way that implies they are the same instrument. Recommended remediation: "(adopted by UN GA Res. 260 A (III), 9 December 1948; entered into force 12 January 1951)."

### L3. *Krstić* Trial Judgment ¶513 citation for (b) threshold

**Where:** Synthesis §4(b), line 90: "(ICTR, *Akayesu*, ¶¶504, 731–734; ICTR, *Kayishema and Ruzindana*, 21 May 1999, ¶¶108–113; ICTY, *Krstić*, Trial Judgment, 2 August 2001, ¶513)."

**Finding:** *Krstić* Trial Judgment ¶513 does discuss serious bodily and mental harm in the genocide context (search-confirmed). The (b) "more than minor or temporary" standard is more squarely articulated in *Kayishema and Ruzindana* ¶¶108-113 and in subsequent ICTY jurisprudence (e.g., *Tolimir*); the *Krstić* ¶513 reference is correct for the threshold language but is one of several places where the doctrine is articulated. No error. Recommended: consider adding ICTY *Tolimir* or *Karadžić* references for cumulative weight. LOW because the citation is correct as far as it goes.

### L4. Schabas quotations: dual-quoted with different source pointers

**Where:** Synthesis §5(d), line 196: "(Schabas, ECPS interview; Anadolu Agency, 2025; Oxford Centre for Criminology Blog, July 2025)." Section 5(d) also quotes "arguably the strongest case of genocide that has ever come before the Court."

**Finding:** The "arguably the strongest case" formulation is from the September 2025 ECPS interview with Schabas (verified). The Anadolu Agency citation is a secondary reproduction. The "Oxford Centre for Criminology Blog, July 2025" reference is not separately verified within this review. Recommended remediation: drop the multiple-aggregator pointer and cite the ECPS interview as primary with date (1 September 2025).

### L5. *Akayesu* paragraph cluster citations

**Where:** Synthesis §2, line 29: "ICTR, *Akayesu*, 2 September 1998, ¶¶500–501" for killing as intentional unlawful homicide; ¶¶504, 731–734 for (b); ¶¶505–506 for (c); ¶¶507–508 for (d).

**Finding:** Paragraph clusters ¶¶505-506 (conditions of life), ¶¶507-508 (measures to prevent births) are search-verified. Paragraphs ¶¶500-501 (killing) and ¶¶731-734 (sexual violence) were not retrievable via direct WebFetch (403); they are widely cited at these paragraph numbers in secondary scholarship. Treat as LOW pending direct verification.

### L6. Spagat sample size and field period precision

**Where:** Synthesis §4(a), line 78: "The Spagat et al. population-representative household survey in *Lancet Global Health* (February 2026) estimated 75,200 violent deaths (95% CI 63,600–86,800) and 16,300 non-violent deaths over 7 October 2023 to 5 January 2025."

**Finding:** Sample size (2,000 households / 200 PSUs / 9,729 individuals) and field period (30 December 2024–5 January 2025) are not included in the synthesis text. Methodology under-described, though the central estimate, CI, period, and population framing are correct. Recommended remediation: add sample size and field period inline.

### L7. WHO/UNICEF polio campaign reach: "roughly 90%"

**Where:** Synthesis §5(c), line 184; executive brief §5, line 55: "approximately 1.1 million doses to roughly 90% of Gaza children."

**Finding:** WHO reports first round vaccinated 559,161 children (≈95% of target) and second round vaccinated 556,774 (~94% of target), totalling roughly 1.116 million administrations to children under 10. "Roughly 90%" is conservative; "approximately 95%" is the WHO-stated reach. Recommended remediation: update to "approximately 94–95%" with WHO citation, or retain "roughly 90%" and note the conservative framing.

### L8. ICJ Advisory Opinion dispositif paragraph

**Where:** Synthesis §3, line 66: "Advisory Opinion, 19 July 2024, dispositif ¶285(3)."

**Finding:** The dispositif of the 19 July 2024 Advisory Opinion is at ¶285 (subdivided). The "¶285(3)" reference targets the unlawful-presence holding. Not separately confirmed via primary text retrieval (403). LOW.

### L9. "Famine is setting in" quotation precision

**Where:** Synthesis §3, line 56: "the Court observed that 'Palestinians in Gaza are no longer facing only a risk of famine ... but that famine is setting in'."

**Finding:** Verified. The fuller quote ("at least 31 people, including 27 children, having already died of malnutrition and dehydration") is omitted; using ellipsis to truncate is acceptable. Paragraph 21 attribution verified. LOW because the ellipsis-bracketed quotation is faithful.

## 5. Items considered and dismissed

### D1. ICJ ¶54 plausibility quote (synthesis §3 and executive brief §3)

The block-quote of paragraph 54 in both the synthesis and the executive brief matches the search-verified text of the 26 January 2024 Order. No deviation.

### D2. ICJ ¶45 "Palestinians appear to constitute a distinct 'national, ethnical, racial or religious group'"

Synthesis §2, line 33, attributes to ¶45. Search-verified.

### D3. ICJ ¶86 "take all measures within its power to prevent the commission" and ¶74 "real and imminent risk"

Both search-consistent with the dispositif and reasoning paragraphs of the 26 January 2024 Order.

### D4. *Croatia v. Serbia* ¶148 "only inference" / *Bosnia v. Serbia* ¶373 "only point" / *Bosnia* ¶209 "fully conclusive"

All three formulations search-verified at the cited paragraph numbers.

### D5. *Bosnia* ¶¶186-189 dolus specialis / discriminatory motive

Verified. Synthesis correctly distinguishes the special intent requirement at ¶187 from the broader analytic structure at ¶¶186-189.

### D6. Gallant 9 October 2023 statement

Verified against multiple secondary reproductions of the IDF/MoD video. Minor wording variance ("we act accordingly" vs. "we are acting accordingly") exists across English translations of the Hebrew; synthesis's choice is defensible.

### D7. Pillay/Sidoti/Kothari attribution for A/HRC/60/CRP.3

Commissioners' names correct; document ID, date (16 September 2025), and title (*Legal analysis of the conduct of Israel in Gaza pursuant to the Convention on the Prevention and Punishment of the Crime of Genocide*) all verified.

### D8. Amnesty *MDE 15/8668/2024*, 5 December 2024, "You Feel Like You Are Subhuman"

ID, date, title, and "22 statements by senior officials" cataloguing all verified.

### D9. HRW *Extermination and Acts of Genocide* (water), 19 December 2024

Verified; 179 pages; quote on "deliberately inflicted conditions of life calculated to bring about the destruction of part of the population in Gaza" verified verbatim against HRW.

### D10. B'Tselem/PHR-Israel *Our Genocide*, 28 July 2025

Date, title, and quote on "coordinated action to intentionally destroy Palestinian society in the Gaza Strip" verified.

### D11. IAGS resolution, 31 August 2025, 86% / 28% turnout

Date and 86% in-favour figure verified. Synthesis says "fulfil the legal definition of genocide"; PBS/JTA reporting renders this as "meet the legal definition." This is a translation choice on a single verb; both "fulfil" and "meet" are defensible English renderings of the resolution. Not flagged.

### D12. UN CoI March 2025 SRGBV report *A/HRC/58/CRP.6*, 13 March 2025

Document ID, date, and "more than a human can bear" series titling verified.

### D13. UN SG CRSV report S/2025/389

Verified: 12 incidents, 7 Palestinian male detainees, one rape, one attempted rape, three incidents of squeezing/pulling of genitals, seven of kicking/beating of genitals.

### D14. Patten mission report, 4 March 2024, *South Africa v. Israel* paragraph cluster references

Patten date verified. Synthesis correctly notes Patten findings "fell below" beyond-reasonable-doubt criminal threshold.

### D15. Bartov NYT op-ed, 15 July 2025, "inescapable conclusion"

Date, outlet, quote verified.

### D16. Nicaragua v. Germany, 15-1, 30 April 2024

Verified.

### D17. ICJ Advisory Opinion of 19 July 2024, 11-4

Verified.

### D18. UNOSAT October 2025: 81%, 123,464 destroyed, 198,273 affected, 320,622 housing units

Verified.

### D19. *Krstić* Appeals Judgment, 19 April 2004, ¶¶8-14 "substantial part" criteria

Substantial-part doctrine at this paragraph cluster is consistent with secondary scholarship. Not directly retrieved (PDF 403). Provisionally accepted.

### D20. Executive Order 14203, February 2025

Verified (signed 6 February 2025; OFAC designation of Karim Khan 13 February 2025).

### D21. IPC Phase 5 confirmation, 22 August 2025, Gaza Governorate, 641,000 in Catastrophe

Verified.

### D22. Khatib/McKee/Yusuf Lancet correspondence, 5 July 2024, 186,000

Authors, date, 4:1 ratio, 37,396 baseline, 186,000 extrapolation all verified.

### D23. Jamaluddine et al. capture-recapture, 64,260 (CI 55,298–78,525), Lancet

Verified. Publication date listed as 9 January 2025 in synthesis is consistent with the PubMed PIIS0140-6736(24)02678-3 record (early-online January 2025).

### D24. Sde Teiman MAG sequence

The synthesis's account ("the MAG opened investigations, then resigned amid backlash, and her successor withdrew the criminal charges against five reservists") matches the IDI Lawfare account: Maj.-Gen. Yifat Tomer-Yerushalmi filed indictments 19 February 2025; her successor Maj.-Gen. Itay Ofir withdrew them on 12 March 2026. Verified.

### D25. Lavender / Where's Daddy / +972/Local Call, 3 April 2024, "six anonymous Israeli intelligence officers"

Date, outlet, source-count verified.

### D26. *Gambia v. Myanmar* provisional measures, 23 January 2020, ¶¶43–58 / ¶¶30, 56

Plausibility / "capable of falling within" framework verified at this paragraph cluster.

### D27. *Gambia v. Myanmar* Preliminary Objections, 22 July 2022, ¶¶107–114

Erga omnes partes ruling verified at this paragraph cluster.

### D28. Belgium Article 63 declaration, 23 December 2025

Verified.

### D29. 7 October 2023 fatality figures

Synthesis says "approximately 1,195 in Israel (widely rounded to 1,200), of whom at least 828 were civilians (including 36 children and 71 foreign nationals), and at least 367 security personnel; approximately 251 persons were taken hostage." The 1,195/824–828 civilian/36 children/251 hostage figures are consistent with cross-referenced Amnesty and Israeli MFA reporting. Synthesis's "71 foreign nationals" not separately verified in this review (search did not surface that specific subfigure); treat as retrieval gap below. Hostage figure of 251 verified.

## 6. Retrieval gaps

Citations where primary-source retrieval failed (typically HTTP 403 against the canonical primary domain) and only secondary or summary text was available:

1. **ICJ Order of 26 January 2024 PDF** (icj-cij.org). Direct text of ¶¶30, 45, 54, 74, 86 verified via UN/UNISPAL and EJIL-Talk excerpts, not via direct ICJ PDF retrieval.
2. **ICC Press Release of 21 November 2024** (icc-cpi.int). Direct retrieval blocked; verification via UN News and secondary reproductions.
3. **OHCHR press release of 16 September 2025 and A/HRC/60/CRP.3 PDF** (ohchr.org, un.org/unispal). Direct retrieval blocked; Pillay-attribution quote sourced via secondary aggregators that themselves quote the press release.
4. **UNFPA Situation Report May/June 2025** (un.org/unispal). Direct retrieval blocked; UNFPA news release of 23 July 2025 covers the same statistics.
5. **South Africa's Application of 29 December 2023** (icj-cij.org). Direct paragraph numbering (¶¶99, 101–104, 110, 111, 99–127, 144) sourced via upstream agent 2 only, not against the Application PDF itself.
6. **South Africa's Memorial of 28 October 2024** (not public). 750-page / ~4,000-page-annex figures sourced via DIRCO statement (named) but no document retrieval.
7. **Israel's Counter-Memorial of 12 March 2026** (confidential). Date sourced via DIRCO statement; document itself not public.
8. *Akayesu* Trial Judgment full text (un.org / hrlibrary.umn.edu, both 403). Paragraph ¶¶500-501, ¶¶731-734 not directly retrieved.
9. *Krstić* Trial Judgment ¶513 (icty.org, 403). Verified via secondary case-law databases only.
10. *Krstić* Appeals Judgment ¶¶8-14 (cld.irmct.org, 403). Not directly retrieved.
11. **Synthesis's "71 foreign nationals" subfigure for 7 October fatalities** not surfaced in search digests for this review.

## 7. Whitelist compliance

The plan whitelist (`00_plan.md`) admits: ICJ/ICC, UN bodies, ICRC, named human rights organisations (Amnesty, HRW, B'Tselem, PHR-Israel, ICJ-Geneva), peer-reviewed journals, Israeli government/IDF Spokesperson channels, Hamas official statements, named scholars in peer-reviewed publications or major outlets. Excluded: partisan blogs, social media (except verified official accounts), anonymous sources, advocacy aggregators without primary sourcing.

Citations within the synthesis and brief that fall outside the whitelist as cited:

### W1. Haaretz (29 January 2026) and CNN (30 January 2026) as primary citations for the IDF 70,000 estimate

Cross-referenced under M6 above. Haaretz and CNN are not whitelisted. The synthesis does not appear to have an alternative whitelisted primary (the IDF Spokesperson's response is whitelisted but does not confirm the figure; it disclaims it). Recommended remediation: retain Haaretz/CNN but inline-flag as "non-whitelisted reporting; IDF Spokesperson disclaimed the figure as 'not reflecting official IDF data'," or seek a Yedioth Ahronoth / Kan 11 official primary that may also fall outside the whitelist.

### W2. Times of Israel and Reuters as transcription sources for Gallant 9 October 2023 statement

Synthesis §5(a), line 158: "(IDF/MoD video, 9 October 2023; transcribed by Times of Israel, Reuters)." Times of Israel and Reuters are not on the whitelist. The primary IDF/MoD video is on-whitelist (IDF Spokesperson channels). Recommended remediation: cite the IDF/MoD primary alone, drop the Times of Israel/Reuters secondary aggregator pointer (the transcription is uncontested).

Borderline items examined and not flagged as violations:
- The IPC and Famine Review Committee are UN-coordinated bodies; counted as on-whitelist.
- DIRCO statements (South African Department of International Relations and Cooperation) are State-party communications relating to ICJ proceedings; counted as adjacent to "ICJ filings" and not flagged.
- Israel MFA statements (e.g., "Israel MFA, 14 March 2026") are Israeli government official statements; on-whitelist.
- MEMRI transcript of Ghazi Hamad LBC interview (synthesis §5(e)) is a translation aggregator; the underlying LBC TV broadcast is the primary. MEMRI is contested as an aggregator. Synthesis citation reads "(LBC TV; MEMRI transcript)" which dual-cites; LBC is the primary and on the "major outlets" reading. Not flagged.
- ECPS, Anadolu Agency, Oxford Centre for Criminology Blog used for Schabas attribution (synthesis §5(d)): each is a publication channel for a named scholar's interview/op-ed. On the "named scholars in peer-reviewed publications or major outlets" reading, the ECPS interview is the primary scholar-channel. LOW under L4; not a whitelist violation.

---

*End of memo. Reviewer recommends remediation of H1 before publication, and inline corrections for M1, M2, M4, M6/W1, and W2 before publication. Other items are non-blocking.*
