import { g as re, w as x } from "./Index-drch552Z.js";
const w = window.ms_globals.React, O = window.ms_globals.React.useMemo, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Calendar, N = window.ms_globals.dayjs;
var q = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = w, se = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, e, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) ce.call(e, l) && !de.hasOwnProperty(l) && (r[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) r[l] === void 0 && (r[l] = e[l]);
  return {
    $$typeof: se,
    type: n,
    key: t,
    ref: s,
    props: r,
    _owner: ae.current
  };
}
k.Fragment = ie;
k.jsx = B;
k.jsxs = B;
q.exports = k;
var J = q.exports;
const {
  SvelteComponent: ue,
  assign: W,
  binding_callbacks: M,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: _e,
  component_subscribe: z,
  compute_slots: pe,
  create_slot: me,
  detach: v,
  element: X,
  empty: G,
  exclude_internal_props: U,
  get_all_dirty_from_scope: he,
  get_slot_changes: we,
  group_outros: ge,
  init: ye,
  insert_hydration: I,
  safe_not_equal: be,
  set_custom_element_data: Z,
  space: ve,
  transition_in: S,
  transition_out: F,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: Ce,
  onDestroy: Oe,
  setContext: xe
} = window.__gradio__svelte__internal;
function V(n) {
  let e, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = me(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = X("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = Q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      I(t, e, s), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ee(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? we(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : he(
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
      F(r, t), o = !1;
    },
    d(t) {
      t && v(e), r && r.d(t), n[9](null);
    }
  };
}
function Ie(n) {
  let e, o, l, r, t = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      e = X("react-portal-target"), o = ve(), t && t.c(), l = G(), this.h();
    },
    l(s) {
      e = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(v), o = _e(s), t && t.l(s), l = G(), this.h();
    },
    h() {
      Z(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, e, a), n[8](e), I(s, o, a), t && t.m(s, a), I(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && S(t, 1)) : (t = V(s), t.c(), S(t, 1), t.m(l.parentNode, l)) : t && (ge(), F(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(s) {
      r || (S(t), r = !0);
    },
    o(s) {
      F(t), r = !1;
    },
    d(s) {
      s && (v(e), v(o), v(l)), n[8](null), t && t.d(s);
    }
  };
}
function H(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Se(n, e, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const a = pe(t);
  let {
    svelteInit: i
  } = e;
  const h = x(H(e)), u = x();
  z(n, u, (d) => o(0, l = d));
  const p = x();
  z(n, p, (d) => o(1, r = d));
  const c = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: E,
    subSlotIndex: g
  } = re() || {}, y = i({
    parent: f,
    props: h,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: E,
    subSlotIndex: g,
    onDestroy(d) {
      c.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", y), Re(() => {
    h.set(H(e));
  }), Oe(() => {
    c.forEach((d) => d());
  });
  function b(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function P(d) {
    M[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, e = W(W({}, e), U(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = U(e), [l, r, u, p, a, i, s, t, b, P];
}
class ke extends ue {
  constructor(e) {
    super(), ye(this, e, Se, Ie, be, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Pe(n) {
  function e(o) {
    const l = x(), r = new ke({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? L;
          return a.nodes = [...a.nodes, s], K({
            createPortal: A,
            node: L
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), K({
              createPortal: A,
              node: L
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
function Le(n) {
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
function C(n) {
  return O(() => Le(n), [n]);
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const l = n[o];
    return typeof l == "number" && !je.includes(o) ? e[o] = l + "px" : e[o] = l, e;
  }, {}) : {};
}
function D(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(A(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = D(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...t]
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(t);
      e.push(...a), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Ae(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const Fe = $(({
  slot: n,
  clone: e,
  className: o,
  style: l
}, r) => {
  const t = ee(), [s, a] = te([]);
  return ne(() => {
    var p;
    if (!t.current || !n)
      return;
    let i = n;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ae(r, c), o && c.classList.add(...o.split(" ")), l) {
        const f = Te(l);
        Object.keys(f).forEach((_) => {
          c.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let c = function() {
        var g, y, b;
        (g = t.current) != null && g.contains(i) && ((y = t.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: E
        } = D(n);
        return i = E, a(_), i.style.display = "contents", h(), (b = t.current) == null || b.appendChild(i), _.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var c, f;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((f = t.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, o, l, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function De(n, e) {
  return n ? /* @__PURE__ */ J.jsx(Fe, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function j({
  key: n,
  setSlotParams: e,
  slots: o
}, l) {
  return o[n] ? (...r) => (e(n, r), De(o[n], {
    clone: !0,
    ...l
  })) : void 0;
}
function T(n) {
  return N(typeof n == "number" ? n * 1e3 : n);
}
const We = Pe(({
  disabledDate: n,
  value: e,
  defaultValue: o,
  validRange: l,
  onChange: r,
  onPanelChange: t,
  onSelect: s,
  onValueChange: a,
  setSlotParams: i,
  cellRender: h,
  fullCellRender: u,
  headerRender: p,
  slots: c,
  ...f
}) => {
  const _ = C(n), E = C(h), g = C(u), y = C(p), b = O(() => e ? T(e) : void 0, [e]), P = O(() => o ? T(o) : void 0, [o]), d = O(() => Array.isArray(l) ? l.map((m) => T(m)) : void 0, [l]);
  return /* @__PURE__ */ J.jsx(oe, {
    ...f,
    value: b,
    defaultValue: P,
    validRange: d,
    disabledDate: _,
    cellRender: c.cellRender ? j({
      slots: c,
      setSlotParams: i,
      key: "cellRender"
    }) : E,
    fullCellRender: c.fullCellRender ? j({
      slots: c,
      setSlotParams: i,
      key: "fullCellRender"
    }) : g,
    headerRender: c.headerRender ? j({
      slots: c,
      setSlotParams: i,
      key: "headerRender"
    }) : y,
    onChange: (m, ...R) => {
      a(m.valueOf() / 1e3), r == null || r(m.valueOf() / 1e3, ...R);
    },
    onPanelChange: (m, ...R) => {
      t == null || t(m.valueOf() / 1e3, ...R);
    },
    onSelect: (m, ...R) => {
      s == null || s(m.valueOf() / 1e3, ...R);
    }
  });
});
export {
  We as Calendar,
  We as default
};
