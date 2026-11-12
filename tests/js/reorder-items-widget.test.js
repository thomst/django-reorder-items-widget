import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { JSDOM } from "jsdom";

const widgetScript = readFileSync(
  new URL("../../reorder_items_widget/static/js/reorder-items-widget.js", import.meta.url),
  "utf8",
);

function createDOM(markup) {
  let resolveDOMContentLoaded;
  const domReady = new Promise((resolve) => {
    resolveDOMContentLoaded = resolve;
  });
  const dom = new JSDOM(`<!doctype html><html><body>${markup}</body></html>`, {
    runScripts: "outside-only",
    beforeParse(window) {
      window.eval(widgetScript);
      window.document.addEventListener(
        "DOMContentLoaded",
        resolveDOMContentLoaded,
        { once: true },
      );
    },
  });

  return domReady.then(() => dom);
}

function createDataTransfer() {
  const values = new Map();
  return {
    setData(type, value) {
      values.set(type, value);
    },
    getData(type) {
      return values.get(type);
    },
  };
}

function dispatchDragEvent(window, element, type, dataTransfer) {
  const event = new window.Event(type, { bubbles: true, cancelable: true });
  Object.defineProperty(event, "dataTransfer", { value: dataTransfer });
  element.dispatchEvent(event);
  return event;
}

function itemRow(id, index) {
  return `<tr><td><div class="drag-handle"></div>
    <input id="index-${id}" class="reorder-items-widget-index" value="${index}">
  </td></tr>`;
}

function startDragging(window, row) {
  row.querySelector(".drag-handle").dispatchEvent(
    new window.MouseEvent("mousedown", { bubbles: true }),
  );
  const dataTransfer = createDataTransfer();
  dispatchDragEvent(window, row, "dragstart", dataTransfer);
  return dataTransfer;
}

test("dragging a changelist row reorders rows and renumbers indexes on submit", async () => {
  const dom = await createDOM(`
    <form>
      <table id="result_list">
        <thead><tr><th>Item</th></tr></thead>
        <tbody>
          ${itemRow("a", 10)}
          ${itemRow("b", 11)}
          ${itemRow("c", 12)}
        </tbody>
      </table>
    </form>
  `);

  try {
    const { document } = dom.window;
    const table = document.querySelector("#result_list");
    const [first, second, third] = table.querySelectorAll("tbody > tr");
    const dataTransfer = startDragging(dom.window, first);

    assert.equal(first.classList.contains("on-drag"), true);
    assert.equal(dataTransfer.getData("text"), "index-a");

    const dragover = dispatchDragEvent(dom.window, second, "dragover", dataTransfer);
    assert.equal(dragover.defaultPrevented, true);
    dispatchDragEvent(dom.window, second, "drop", dataTransfer);

    assert.deepEqual(
      Array.from(table.querySelectorAll("tbody > tr")),
      [second, first, third],
    );

    document.querySelector("form").dispatchEvent(
      new dom.window.Event("submit", { bubbles: true, cancelable: true }),
    );

    assert.deepEqual(
      Array.from(table.querySelectorAll(".reorder-items-widget-index"), (input) => input.value),
      ["10", "11", "12"],
    );

    dispatchDragEvent(dom.window, first, "dragend", dataTransfer);
    assert.equal(first.classList.contains("on-drag"), false);
    assert.equal(first.getAttribute("draggable"), "false");
  } finally {
    dom.window.close();
  }
});

test("dropping a changelist row on the header moves it to the beginning", async () => {
  const dom = await createDOM(`
    <form>
      <table id="result_list">
        <thead><tr><th>Item</th></tr></thead>
        <tbody>
          ${itemRow("a", 0)}
          ${itemRow("b", 1)}
        </tbody>
      </table>
    </form>
  `);

  try {
    const { document } = dom.window;
    const table = document.querySelector("#result_list");
    const [first, second] = table.querySelectorAll("tbody > tr");
    const header = table.querySelector("thead > tr");
    const dataTransfer = startDragging(dom.window, second);

    const dragover = dispatchDragEvent(dom.window, header, "dragover", dataTransfer);
    assert.equal(dragover.defaultPrevented, true);
    dispatchDragEvent(dom.window, header, "drop", dataTransfer);

    assert.deepEqual(
      Array.from(table.querySelectorAll("tbody > tr")),
      [second, first],
    );
  } finally {
    dom.window.close();
  }
});

test("inline submission skips deleted rows and unchanged extra rows", async () => {
  const inlineRow = (id, index, name, { original = false, deleted = false } = {}) => `
    <tr class="form-row${original ? " has_original" : ""}">
      <td>
        ${original ? '<div class="drag-handle"></div>' : ""}
        <input name="name-${id}" value="${name}">
        <input id="index-${id}" class="reorder-items-widget-index" value="${index}">
      </td>
      ${original ? `<td class="delete"><input type="checkbox" ${deleted ? "checked" : ""}></td>` : ""}
    </tr>
  `;
  const dom = await createDOM(`
    <form>
      <table id="inline-items">
        <thead><tr><th>Item</th></tr></thead>
        <tbody>
          ${inlineRow("saved", 20, "Saved", { original: true })}
          ${inlineRow("deleted", 21, "Deleted", { original: true, deleted: true })}
          ${inlineRow("unchanged", "", "Unchanged")}
          ${inlineRow("changed", "", "Before")}
        </tbody>
      </table>
    </form>
  `);

  try {
    const { document } = dom.window;
    const table = document.querySelector("#inline-items");
    document.querySelector('input[name="name-changed"]').value = "After";

    document.querySelector("form").dispatchEvent(
      new dom.window.Event("submit", { bubbles: true, cancelable: true }),
    );

    assert.equal(document.querySelector("#index-saved").value, "20");
    assert.equal(document.querySelector("#index-deleted").value, "21");
    assert.equal(document.querySelector("#index-unchanged").value, "");
    assert.equal(document.querySelector("#index-changed").value, "21");
    assert.equal(table.querySelectorAll("tbody > tr").length, 4);
  } finally {
    dom.window.close();
  }
});
