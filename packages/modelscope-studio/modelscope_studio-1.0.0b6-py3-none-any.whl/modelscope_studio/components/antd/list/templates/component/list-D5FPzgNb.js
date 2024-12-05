import { g as Z, w as v } from "./Index-Mi0-IJSd.js";
const p = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.List;
var z = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = p, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(t, e, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) re.call(e, s) && !se.hasOwnProperty(s) && (r[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: te,
    type: t,
    key: n,
    ref: l,
    props: r,
    _owner: oe.current
  };
}
x.Fragment = ne;
x.jsx = G;
x.jsxs = G;
z.exports = x;
var w = z.exports;
const {
  SvelteComponent: le,
  assign: j,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: de,
  detach: h,
  element: K,
  empty: A,
  exclude_internal_props: M,
  get_all_dirty_from_scope: ue,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: he,
  transition_in: I,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function F(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = de(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      e = H(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(e);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      C(n, e, l), r && r.m(e, null), t[9](e), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? fe(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (I(r, n), o = !0);
    },
    o(n) {
      k(r, n), o = !1;
    },
    d(n) {
      n && h(e), r && r.d(n), t[9](null);
    }
  };
}
function ve(t) {
  let e, o, s, r, n = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      e = K("react-portal-target"), o = he(), n && n.c(), s = A(), this.h();
    },
    l(l) {
      e = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(e).forEach(h), o = ce(l), n && n.l(l), s = A(), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      C(l, e, c), t[8](e), C(l, o, c), n && n.m(l, c), C(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && I(n, 1)) : (n = F(l), n.c(), I(n, 1), n.m(s.parentNode, s)) : n && (_e(), k(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(l) {
      r || (I(n), r = !0);
    },
    o(l) {
      k(n), r = !1;
    },
    d(l) {
      l && (h(e), h(o), h(s)), t[8](null), n && n.d(l);
    }
  };
}
function W(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function Ce(t, e, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = e;
  const c = ae(n);
  let {
    svelteInit: i
  } = e;
  const g = v(W(e)), u = v();
  N(t, u, (a) => o(0, s = a));
  const m = v();
  N(t, m, (a) => o(1, r = a));
  const d = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: g,
    target: u,
    slot: m,
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b,
    onDestroy(a) {
      d.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", y), we(() => {
    g.set(W(e));
  }), ye(() => {
    d.forEach((a) => a());
  });
  function E(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  function V(a) {
    T[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, e = j(j({}, e), M(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, e = M(e), [s, r, u, m, c, i, l, n, E, V];
}
class Ie extends le {
  constructor(e) {
    super(), me(this, e, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, O = window.ms_globals.tree;
function Se(t) {
  function e(o) {
    const s = v(), r = new Ie({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? O;
          return c.nodes = [...c.nodes, l], D({
            createPortal: P,
            node: O
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
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
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return typeof s == "number" && !xe.includes(o) ? e[o] = s + "px" : e[o] = s, e;
  }, {}) : {};
}
function L(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(P(p.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: p.Children.toArray(t._reactElement.props.children).map((r) => {
        if (p.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(r.props.el);
          return p.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...p.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const n = s[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(n);
      e.push(...c), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Oe(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const S = B(({
  slot: t,
  clone: e,
  className: o,
  style: s
}, r) => {
  const n = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!n.current || !t)
      return;
    let i = t;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Oe(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = Re(s);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let d = function() {
        var b, y, E;
        (b = n.current) != null && b.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: R
        } = L(t);
        return i = R, c(_), i.style.display = "contents", g(), (E = n.current) == null || E.appendChild(i), _.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = n.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = n.current) != null && d.contains(i) && ((f = n.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, e, o, s, r]), p.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(t) {
  try {
    if (typeof t == "string") {
      let e = t.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function ke(t) {
  return X(() => Pe(t), [t]);
}
function Le(t, e) {
  return t ? /* @__PURE__ */ w.jsx(S, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function je({
  key: t,
  setSlotParams: e,
  slots: o
}, s) {
  return o[t] ? (...r) => (e(t, r), Le(o[t], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Se(({
  slots: t,
  renderItem: e,
  setSlotParams: o,
  ...s
}) => {
  const r = ke(e);
  return /* @__PURE__ */ w.jsx($, {
    ...s,
    footer: t.footer ? /* @__PURE__ */ w.jsx(S, {
      slot: t.footer
    }) : s.footer,
    header: t.header ? /* @__PURE__ */ w.jsx(S, {
      slot: t.header
    }) : s.header,
    loadMore: t.loadMore ? /* @__PURE__ */ w.jsx(S, {
      slot: t.loadMore
    }) : s.loadMore,
    renderItem: t.renderItem ? je({
      slots: t,
      setSlotParams: o,
      key: "renderItem"
    }) : r
  });
});
export {
  Ne as List,
  Ne as default
};
