# SSML Reference

All synthesis scripts use SSML (Speech Synthesis Markup Language) under the
hood. The `DragonLatestNeural` personal voice model supports the following.

## Basic Structure

```xml
<speak version='1.0'
       xmlns='http://www.w3.org/2001/10/synthesis'
       xmlns:mstts='http://www.w3.org/2001/mstts'
       xml:lang='en-US'>
    <voice name='DragonLatestNeural'>
        <mstts:ttsembedding speakerProfileId='YOUR-UUID-HERE'>
            Your text here.
        </mstts:ttsembedding>
    </voice>
</speak>
```

## Supported Tags

| Tag | Example | Effect |
|-----|---------|--------|
| `<break>` | `<break time='500ms'/>` | Insert a pause |
| `<prosody rate>` | `<prosody rate='-5%'>...</prosody>` | Slow down or speed up |
| `<prosody pitch>` | `<prosody pitch='+2%'>...</prosody>` | Raise or lower pitch |
| `<p>` | `<p>Paragraph text</p>` | Paragraph boundary |
| `<s>` | `<s>A sentence.</s>` | Sentence boundary |
| `<say-as>` | `<say-as interpret-as='date'>2026-04-15</say-as>` | Interpret as date/number/etc |
| `<sub>` | `<sub alias='CES three'>CES3</sub>` | Pronunciation substitution |
| `<lang>` | `<lang xml:lang='it-IT'>Ciao mondo</lang>` | Speak in another language |

## Multi-Language Workaround

The `DragonLatestNeural` model does **not** support changing the top-level
`xml:lang` attribute to a non-English locale (returns a 500 error). To generate
speech in another language, keep `xml:lang='en-US'` at the top level and use
the `<lang>` tag inside the SSML body:

```xml
<speak version='1.0'
       xmlns='http://www.w3.org/2001/10/synthesis'
       xmlns:mstts='http://www.w3.org/2001/mstts'
       xml:lang='en-US'>
    <voice name='DragonLatestNeural'>
        <mstts:ttsembedding speakerProfileId='YOUR-UUID'>
            <lang xml:lang='it-IT'>
                Ciao mondo, questo e un test della voce clonata.
            </lang>
        </mstts:ttsembedding>
    </voice>
</speak>
```

This must be called via the Azure API directly (curl), not through
`synthesize.sh` which hardcodes `xml:lang='en-US'` without the `<lang>` wrapper.

## SSML with Enhanced Narration

For longer narration, use SSML to add pauses between paragraphs, vary pacing,
and structure the speech naturally:

```xml
<speak version='1.0'
       xmlns='http://www.w3.org/2001/10/synthesis'
       xmlns:mstts='http://www.w3.org/2001/mstts'
       xml:lang='en-US'>
    <voice name='DragonLatestNeural'>
        <mstts:ttsembedding speakerProfileId='UUID'>
            <p><s>First paragraph, first sentence.</s>
            <s>First paragraph, second sentence.</s></p>
            <break time='800ms'/>
            <p><prosody rate='-3%'>
                Second paragraph, slightly slower for emphasis.
            </prosody></p>
        </mstts:ttsembedding>
    </voice>
</speak>
```

Tips:
- Use `<p>` and `<s>` tags for natural paragraph/sentence boundaries
- Add `<break time='600ms'/>` between paragraphs for breathing room
- Use `<prosody rate='-5%'>` to slow down important sections
- Use `<sub alias='...'>` for acronyms and technical terms
