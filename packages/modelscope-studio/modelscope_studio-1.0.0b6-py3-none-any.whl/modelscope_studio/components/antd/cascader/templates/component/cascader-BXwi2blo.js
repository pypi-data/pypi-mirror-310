import { b as fe, g as _e, w as S } from "./Index-BqvBD3wy.js";
const x = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, T = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, L = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.antd.Cascader;
function pe(e, t) {
  return fe(e, t);
}
var K = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = x, ge = Symbol.for("react.element"), we = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ye = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, t, l) {
  var r, o = {}, n = null, s = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) be.call(t, r) && !Ee.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: ge,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: ye.current
  };
}
O.Fragment = we;
O.jsx = Q;
O.jsxs = Q;
K.exports = O;
var g = K.exports;
const {
  SvelteComponent: xe,
  assign: W,
  binding_callbacks: M,
  check_outros: Ce,
  children: X,
  claim_element: Z,
  claim_space: Re,
  component_subscribe: q,
  compute_slots: Ie,
  create_slot: ve,
  detach: I,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Se,
  get_slot_changes: ke,
  group_outros: je,
  init: Oe,
  insert_hydration: k,
  safe_not_equal: Fe,
  set_custom_element_data: ee,
  space: Pe,
  transition_in: j,
  transition_out: A,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Le,
  getContext: Ne,
  onDestroy: Ae,
  setContext: De
} = window.__gradio__svelte__internal;
function U(e) {
  let t, l;
  const r = (
    /*#slots*/
    e[7].default
  ), o = ve(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Z(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(t);
      o && o.l(s), s.forEach(I), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), o && o.m(t, null), e[9](t), l = !0;
    },
    p(n, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && Te(
        o,
        r,
        n,
        /*$$scope*/
        n[6],
        l ? ke(
          r,
          /*$$scope*/
          n[6],
          s,
          null
        ) : Se(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (j(o, n), l = !0);
    },
    o(n) {
      A(o, n), l = !1;
    },
    d(n) {
      n && I(t), o && o.d(n), e[9](null);
    }
  };
}
function Ve(e) {
  let t, l, r, o, n = (
    /*$$slots*/
    e[4].default && U(e)
  );
  return {
    c() {
      t = $("react-portal-target"), l = Pe(), n && n.c(), r = z(), this.h();
    },
    l(s) {
      t = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(t).forEach(I), l = Re(s), n && n.l(s), r = z(), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      k(s, t, a), e[8](t), k(s, l, a), n && n.m(s, a), k(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, a), a & /*$$slots*/
      16 && j(n, 1)) : (n = U(s), n.c(), j(n, 1), n.m(r.parentNode, r)) : n && (je(), A(n, 1, 1, () => {
        n = null;
      }), Ce());
    },
    i(s) {
      o || (j(n), o = !0);
    },
    o(s) {
      A(n), o = !1;
    },
    d(s) {
      s && (I(t), I(l), I(r)), e[8](null), n && n.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function We(e, t, l) {
  let r, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const a = Ie(n);
  let {
    svelteInit: c
  } = t;
  const m = S(H(t)), d = S();
  q(e, d, (u) => l(0, r = u));
  const _ = S();
  q(e, _, (u) => l(1, o = u));
  const i = [], h = Ne("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: w,
    subSlotIndex: p
  } = _e() || {}, C = c({
    parent: h,
    props: m,
    target: d,
    slot: _,
    slotKey: f,
    slotIndex: w,
    subSlotIndex: p,
    onDestroy(u) {
      i.push(u);
    }
  });
  De("$$ms-gr-react-wrapper", C), Le(() => {
    m.set(H(t));
  }), Ae(() => {
    i.forEach((u) => u());
  });
  function R(u) {
    M[u ? "unshift" : "push"](() => {
      r = u, d.set(r);
    });
  }
  function F(u) {
    M[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    l(17, t = W(W({}, t), G(u))), "svelteInit" in u && l(5, c = u.svelteInit), "$$scope" in u && l(6, s = u.$$scope);
  }, t = G(t), [r, o, d, _, a, c, s, n, R, F];
}
class Me extends xe {
  constructor(t) {
    super(), Oe(this, t, We, Ve, Fe, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, P = window.ms_globals.tree;
function qe(e) {
  function t(l) {
    const r = S(), o = new Me({
      ...l,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? P;
          return a.nodes = [...a.nodes, s], B({
            createPortal: N,
            node: P
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), B({
              createPortal: N,
              node: P
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const r = e[l];
    return typeof r == "number" && !ze.includes(l) ? t[l] = r + "px" : t[l] = r, t;
  }, {}) : {};
}
function D(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(N(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: x.Children.toArray(e._reactElement.props.children).map((o) => {
        if (x.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(o.props.el);
          return x.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...x.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      l.addEventListener(a, s, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const n = r[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(n);
      t.push(...a), l.appendChild(s);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function Ue(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = ue(({
  slot: e,
  clone: t,
  className: l,
  style: r
}, o) => {
  const n = T(), [s, a] = J([]);
  return L(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function m() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ue(o, i), l && i.classList.add(...l.split(" ")), r) {
        const h = Ge(r);
        Object.keys(h).forEach((f) => {
          i.style[f] = h[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var p, C, R;
        (p = n.current) != null && p.contains(c) && ((C = n.current) == null || C.removeChild(c));
        const {
          portals: f,
          clonedElement: w
        } = D(e);
        return c = w, a(f), c.style.display = "contents", m(), (R = n.current) == null || R.appendChild(c), f.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var i, h;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((h = n.current) == null || h.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, t, l, r, o]), x.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function He(e) {
  try {
    if (typeof e == "string") {
      let t = e.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function b(e) {
  return Y(() => He(e), [e]);
}
function Be({
  value: e,
  onValueChange: t
}) {
  const [l, r] = J(e), o = T(t);
  o.current = t;
  const n = T(l);
  return n.current = l, L(() => {
    o.current(l);
  }, [l]), L(() => {
    pe(e, n.current) || r(e);
  }, [e]), [l, r];
}
function te(e, t, l) {
  return e.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const n = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (l ? `${l}-${o}` : `${o}`)
    };
    let s = n;
    Object.keys(r.slots).forEach((m) => {
      if (!r.slots[m] || !(r.slots[m] instanceof Element) && !r.slots[m].el)
        return;
      const d = m.split(".");
      d.forEach((w, p) => {
        s[w] || (s[w] = {}), p !== d.length - 1 && (s = n[w]);
      });
      const _ = r.slots[m];
      let i, h, f = (t == null ? void 0 : t.clone) ?? !1;
      _ instanceof Element ? i = _ : (i = _.el, h = _.callback, f = _.clone ?? !1), s[d[d.length - 1]] = i ? h ? (...w) => (h(d[d.length - 1], w), /* @__PURE__ */ g.jsx(y, {
        slot: i,
        clone: f
      })) : /* @__PURE__ */ g.jsx(y, {
        slot: i,
        clone: f
      }) : s[d[d.length - 1]], s = n;
    });
    const a = (t == null ? void 0 : t.children) || "children";
    return r[a] && (n[a] = te(r[a], t, `${o}`)), n;
  });
}
function Je(e, t) {
  return e ? /* @__PURE__ */ g.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function v({
  key: e,
  setSlotParams: t,
  slots: l
}, r) {
  return l[e] ? (...o) => (t(e, o), Je(l[e], {
    clone: !0,
    ...r
  })) : void 0;
}
function Ye(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Qe = qe(({
  slots: e,
  children: t,
  onValueChange: l,
  onChange: r,
  displayRender: o,
  elRef: n,
  getPopupContainer: s,
  tagRender: a,
  maxTagPlaceholder: c,
  dropdownRender: m,
  optionRender: d,
  showSearch: _,
  optionItems: i,
  options: h,
  setSlotParams: f,
  onLoadData: w,
  ...p
}) => {
  const C = b(s), R = b(o), F = b(a), u = b(d), ne = b(m), re = b(c), oe = typeof _ == "object" || e["showSearch.render"], E = Ye(_), le = b(E.filter), se = b(E.render), ce = b(E.sort), [ae, ie] = Be({
    onValueChange: l,
    value: p.value
  });
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(he, {
      ...p,
      ref: n,
      value: ae,
      options: Y(() => h || te(i, {
        clone: !0
      }), [h, i]),
      showSearch: oe ? {
        ...E,
        filter: le || E.filter,
        render: e["showSearch.render"] ? v({
          slots: e,
          setSlotParams: f,
          key: "showSearch.render"
        }) : se || E.render,
        sort: ce || E.sort
      } : _,
      loadData: w,
      optionRender: u,
      getPopupContainer: C,
      dropdownRender: e.dropdownRender ? v({
        slots: e,
        setSlotParams: f,
        key: "dropdownRender"
      }) : ne,
      displayRender: e.displayRender ? v({
        slots: e,
        setSlotParams: f,
        key: "displayRender"
      }) : R,
      tagRender: e.tagRender ? v({
        slots: e,
        setSlotParams: f,
        key: "tagRender"
      }) : F,
      onChange: (V, ...de) => {
        r == null || r(V, ...de), ie(V);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.suffixIcon
      }) : p.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.expandIcon
      }) : p.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.removeIcon
      }) : p.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(y, {
        slot: e.notFoundContent
      }) : p.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? v({
        slots: e,
        setSlotParams: f,
        key: "maxTagPlaceholder"
      }) : re || c,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : p.allowClear
    })]
  });
});
export {
  Qe as Cascader,
  Qe as default
};
