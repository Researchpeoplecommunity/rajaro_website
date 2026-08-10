(function () {
  if (typeof TomSelect === "undefined") return;

  function initOfferingSelect(selectEl) {
    var formId = selectEl.dataset.formId;
    var resultId = selectEl.dataset.resultId;

    var ts = new TomSelect(selectEl, {
      plugins: ["remove_button"],
      maxOptions: null,
      placeholder: "Type to search products or services…",
      hideSelected: true,
      closeAfterSelect: false,
      searchField: ["text", "optgroup"],
      render: {
        optgroup_header: function (data, escape) {
          return '<div class="ts-optgroup-header">' + escape(data.label) + "</div>";
        },
      },
    });

    if (formId && resultId) {
      document.body.addEventListener("htmx:afterSwap", function (event) {
        if (event.detail.target.id !== resultId) return;
        var success = event.detail.target.querySelector(".alert-success");
        if (!success) return;
        var form = document.getElementById(formId);
        if (form) form.reset();
        ts.clear();
      });
    }

    return ts;
  }

  document.querySelectorAll("[data-offering-select]").forEach(initOfferingSelect);
})();
