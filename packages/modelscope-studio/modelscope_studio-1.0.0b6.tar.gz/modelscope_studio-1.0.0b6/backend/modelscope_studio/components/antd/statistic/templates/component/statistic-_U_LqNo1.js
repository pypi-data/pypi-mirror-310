import { g as Z, w as v } from "./Index-B0GqX2w2.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Statistic;
var z = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) re.call(e, s) && !se.hasOwnProperty(s) && (r[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: te,
    type: n,
    key: t,
    ref: l,
    props: r,
    _owner: oe.current
  };
}
R.Fragment = ne;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var p = z.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: K,
  empty: A,
  exclude_internal_props: F,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: q,
  space: he,
  transition_in: S,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function W(n) {
  let e, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = H(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(e);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      x(t, e, l), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? fe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : de(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (S(r, t), o = !0);
    },
    o(t) {
      k(r, t), o = !1;
    },
    d(t) {
      t && g(e), r && r.d(t), n[9](null);
    }
  };
}
function ve(n) {
  let e, o, s, r, t = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      e = K("react-portal-target"), o = he(), t && t.c(), s = A(), this.h();
    },
    l(l) {
      e = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(e).forEach(g), o = ce(l), t && t.l(l), s = A(), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, e, c), n[8](e), x(l, o, c), t && t.m(l, c), x(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = W(l), t.c(), S(t, 1), t.m(s.parentNode, s)) : t && (_e(), k(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(l) {
      r || (S(t), r = !0);
    },
    o(l) {
      k(t), r = !1;
    },
    d(l) {
      l && (g(e), g(o), g(s)), n[8](null), t && t.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function xe(n, e, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ae(t);
  let {
    svelteInit: i
  } = e;
  const w = v(D(e)), d = v();
  N(n, d, (a) => o(0, s = a));
  const m = v();
  N(n, m, (a) => o(1, r = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: w,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", y), we(() => {
    w.set(D(e));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    T[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, e = L(L({}, e), F(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, e = F(e), [s, r, d, m, c, i, l, t, E, V];
}
class Se extends le {
  constructor(e) {
    super(), pe(this, e, xe, ve, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function e(o) {
    const s = v(), r = new Se({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? O;
          return c.nodes = [...c.nodes, l], M({
            createPortal: P,
            node: O
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const s = n[o];
    return typeof s == "number" && !Re.includes(o) ? e[o] = s + "px" : e[o] = s, e;
  }, {}) : {};
}
function j(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = j(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...h.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(t);
      e.push(...c), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const C = B(({
  slot: n,
  clone: e,
  className: o,
  style: s
}, r) => {
  const t = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!t.current || !n)
      return;
    let i = n;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Ie(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = t.current) != null && b.contains(i) && ((y = t.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = j(n);
        return i = I, c(_), i.style.display = "contents", w(), (E = t.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, o, s, r]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(n) {
  try {
    if (typeof n == "string") {
      let e = n.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function ke(n) {
  return X(() => Pe(n), [n]);
}
function je(n, e) {
  return n ? /* @__PURE__ */ p.jsx(C, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: o
}, s) {
  return o[n] ? (...r) => (e(n, r), je(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Ce(({
  children: n,
  slots: e,
  setSlotParams: o,
  formatter: s,
  ...r
}) => {
  const t = ke(s);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx($, {
      ...r,
      formatter: e.formatter ? Le({
        slots: e,
        setSlotParams: o,
        key: "formatter"
      }) : t,
      title: e.title ? /* @__PURE__ */ p.jsx(C, {
        slot: e.title
      }) : r.title,
      prefix: e.prefix ? /* @__PURE__ */ p.jsx(C, {
        slot: e.prefix
      }) : r.prefix,
      suffix: e.suffix ? /* @__PURE__ */ p.jsx(C, {
        slot: e.suffix
      }) : r.suffix
    })]
  });
});
export {
  Ne as Statistic,
  Ne as default
};
