const {
  SvelteComponent: b,
  add_iframe_resize_listener: y,
  add_render_callback: h,
  append: m,
  binding_callbacks: v,
  detach: w,
  element: z,
  init: k,
  insert: p,
  noop: u,
  safe_not_equal: S,
  set_data: q,
  text: C,
  toggle_class: d
} = window.__gradio__svelte__internal, { onMount: E } = window.__gradio__svelte__internal;
function M(l) {
  let e, i = (
    /*value*/
    (l[0] ? (
      /*value*/
      l[0]
    ) : "") + ""
  ), _, r;
  return {
    c() {
      e = z("div"), _ = C(i), h(() => (
        /*div_elementresize_handler*/
        l[5].call(e)
      )), d(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), d(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), d(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    m(t, n) {
      p(t, e, n), m(e, _), r = y(
        e,
        /*div_elementresize_handler*/
        l[5].bind(e)
      ), l[6](e);
    },
    p(t, [n]) {
      n & /*value*/
      1 && i !== (i = /*value*/
      (t[0] ? (
        /*value*/
        t[0]
      ) : "") + "") && q(_, i), n & /*type*/
      2 && d(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), n & /*type*/
      2 && d(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), n & /*selected*/
      4 && d(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    i: u,
    o: u,
    d(t) {
      t && w(e), r(), l[6](null);
    }
  };
}
function P(l, e, i) {
  let { value: _ } = e, { type: r } = e, { selected: t = !1 } = e, n, a;
  function f(s, o) {
    !s || !o || (a.style.setProperty("--local-text-width", `${o < 150 ? o : 200}px`), i(4, a.style.whiteSpace = "unset", a));
  }
  E(() => {
    console.log(a, n), f(a, n);
  });
  function c() {
    n = this.clientWidth, i(3, n);
  }
  function g(s) {
    v[s ? "unshift" : "push"](() => {
      a = s, i(4, a);
    });
  }
  return l.$$set = (s) => {
    "value" in s && i(0, _ = s.value), "type" in s && i(1, r = s.type), "selected" in s && i(2, t = s.selected);
  }, [_, r, t, n, a, c, g];
}
class W extends b {
  constructor(e) {
    super(), k(this, e, P, M, S, { value: 0, type: 1, selected: 2 });
  }
}
export {
  W as default
};
