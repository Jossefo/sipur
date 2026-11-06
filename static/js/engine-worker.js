/* Run the existing Python narrative engine in a worker: no story leaves the browser. */
const PYODIDE_ROOT = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";
let ready;
async function engine(base) {
  if (!ready) ready = (async () => {
    const {loadPyodide} = await import(PYODIDE_ROOT + "pyodide.mjs");
    const py = await loadPyodide({indexURL:PYODIDE_ROOT});
    py.FS.mkdirTree("/sipur/data");
    const files = ["story_generator.py", "story_catalog.py", "narrative.py", "illustrator.py", "data/templates.json"];
    await Promise.all(files.map(async path => {
      const response = await fetch(new URL(path, base));
      if (!response.ok) throw new Error("Cannot load story engine");
      py.FS.writeFile("/sipur/" + path, await response.text(), {encoding:"utf8"});
    }));
    await py.runPythonAsync(`
import sys, json
sys.path.insert(0, '/sipur')
from story_generator import generate_story, validate_input, encode_story, decode_story
from illustrator import page_svg, page_image_url

def browser_book(raw):
    data = json.loads(raw)
    if data['action'] == 'generate':
        values = data['values']
        errors = validate_input(values['name'], values['age'], values['events'])
        if errors:
            raise ValueError(' '.join(errors))
        story = generate_story(values['name'], int(values['age']), values['events'],
                               used_template_ids=data.get('used_templates', []),
                               used_fingerprints=data.get('used_fingerprints', []))
    else:
        story = decode_story(data['token'])
    seed = story.get('seed') or 1
    art = [{'svg': page_svg(page, story['name'], seed, story.get('companion') or 'moon', i),
            'image': page_image_url(page, seed, i)} for i, page in enumerate(story['pages'])]
    return json.dumps({'story':story, 'token':encode_story(story), 'art':art}, ensure_ascii=False)
`);
    return py;
  })().catch(error => { ready = null; throw error; });
  return ready;
}
self.onmessage = async event => {
  const {id, base, ...request} = event.data;
  try {
    const py = await engine(base);
    py.globals.set("browser_request_json", JSON.stringify(request));
    const output = await py.runPythonAsync("browser_book(browser_request_json)");
    py.globals.delete("browser_request_json");
    self.postMessage({id, result:JSON.parse(output)});
  } catch (_) { self.postMessage({id, error:"לא הצלחנו להכין את הסיפור. בדקו את החיבור ונסו שוב."}); }
};
