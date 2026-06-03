/**
 * Защита публичного сайта: снимает режим редактирования конструктора,
 * если он случайно попал в сохранённые шаблоны.
 */
(function () {
    "use strict";

    function stripEditArtifacts(root) {
        if (!root) return;
        try {
            if (root === document && document.designMode) {
                document.designMode = "off";
            }
        } catch (e) {
            /* ignore */
        }
        root.querySelectorAll("[contenteditable]").forEach(function (el) {
            el.removeAttribute("contenteditable");
            el.removeAttribute("spellcheck");
        });
        root.querySelectorAll("#constructor-editable-body").forEach(function (el) {
            el.removeAttribute("id");
        });
        root.querySelectorAll("[data-constructor-preview-root], [data-constructor-chrome]").forEach(function (el) {
            el.removeAttribute("data-constructor-preview-root");
            el.removeAttribute("data-constructor-chrome");
        });
        root.querySelectorAll("[data-constructor-slider-preview]").forEach(function (el) {
            el.removeAttribute("data-constructor-slider-preview");
        });
        root.querySelectorAll(".constructor-slide-preview-active").forEach(function (el) {
            el.classList.remove("constructor-slide-preview-active");
        });
        var leakedStyle = document.getElementById("constructor-preview-editor-style");
        if (leakedStyle) leakedStyle.remove();
    }

    function run() {
        stripEditArtifacts(document);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", run);
    } else {
        run();
    }
})();
