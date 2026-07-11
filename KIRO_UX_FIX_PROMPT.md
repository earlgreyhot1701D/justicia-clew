Paste this to Kiro now. Four fixes, in priority order. Do them in order, don't skip ahead, and report back what you actually changed in each file when done, not a summary, the real diff or the real function content.

---

## 1. Question input doesn't clear when going back

In `frontend/app.js`, `$('answerBack').addEventListener('click', () => show('questionScreen'));` just switches screens, it never clears the typed question. Same likely issue on `$('homeBtn')` and `.toLanding` clicks, whatever the user typed should not still be sitting in the box when they come back to ask something new.

Fix: when navigating back to `questionScreen` or `landing`, clear `$('question').value = ''` and re-disable the ask button (`$('ask').disabled = true`), matching the same disabled-until-typed behavior it has on first load.

## 2. Answer text is a wall of text

`openAnswer()` currently does `ansP.textContent = data.answer;` and `p.textContent = data.message;` for refusals, dumping the whole response into one `<p>`. If the agent's response has natural paragraph breaks (`\n`), those collapse in HTML and it reads as one dense block.

Fix: still `textContent` only, never `innerHTML`, that rule doesn't change. Write a small helper that splits the text on newlines, filters out empty lines, and appends one `<p>` per line/paragraph, each set via `textContent`:

```js
function renderParagraphs(container, text) {
  text.split('\n').map(s => s.trim()).filter(Boolean).forEach(line => {
    const p = document.createElement('p');
    p.textContent = line;
    container.appendChild(p);
  });
}
```

Use this in place of the single `ansP.textContent = data.answer` and the refusal's `p.textContent = data.message`, appending to `answerBlock` / `box` instead of building one paragraph node.

## 3. Phone numbers need office hours attached

Right now a refusal shows a phone number with nothing about when someone actually answers it. Someone calling at 7pm gets nothing and that's a bad experience we can easily prevent.

Backend: in `backend/models/schemas.py`, add an `hours` field to `RefusalResponse` (string). In `backend/services/agent_client.py`, add a lookup next to `_get_jury_phone()`:

```python
def _get_jury_hours(county_prefix: str) -> str:
    """Return office hours to pair with the jury phone number."""
    hours = {
        "SB": "Mon-Fri, 8am-3pm, excluding holidays. Automated info line answers anytime: 877-544-5094.",
    }
    return hours.get(county_prefix, "Check your summons for office hours.")
```

Populate `hours` in the refusal dict returned from `_parse_agent_response()` alongside the existing `phone` key.

Frontend: in `frontend/app.js`, right after the existing refusal `call` link is appended, add the hours as its own line under it:

```js
if (data.hours) {
  const hours = document.createElement('p');
  hours.className = 'hours';
  hours.textContent = data.hours;
  box.appendChild(hours);
}
```

Also fix the hardcoded fallback in the network-error `catch` block at the bottom of `openAnswer()`, it currently shows `(805) 882-4530` with no hours either. Add the same hours line there using the SB values above.

Add the Spanish equivalent line for `hours` too, matching the pattern already used for the other bilingual strings in this file.

## 4. Hide FAQ chips that don't have a real answer yet

Some chips currently always refuse because the knowledge base has no content to answer them, not a bug, just not built yet. Showing them as tappable chips sets an expectation the app can't meet right now.

Test all 10 chips in `data/faq_chips.json` against the live agent (use `test_sb_agent.py` as a pattern, or test manually against the deployed URL). For any chip that comes back as a flat refusal with no real grounded content behind it, remove that entry from `data/faq_chips.json` entirely, don't just hide it with CSS, it shouldn't be requested if it can't be answered. Note: `chip-3` (employer) and `chip-5` (postponement) should now work after the knowledge base update earlier, they should very likely stay, but test them for real rather than assuming.

Chips I expect to fail and should be removed if they do: `chip-1` ("Do I still have to go tomorrow?"), `chip-2` ("What happens if I don't show up?"), `chip-4` ("How much do I get paid for jury service?"), `chip-9` ("Can I bring my phone to the courthouse?"), `chip-10` ("What if I have a medical condition?"). Don't remove any of these on my say-so alone, actually run the question against the agent first and remove only the ones that genuinely come back unhelpful.

Report back: which chips got removed, and paste the actual current content of `data/faq_chips.json` afterward so it can be confirmed directly.
