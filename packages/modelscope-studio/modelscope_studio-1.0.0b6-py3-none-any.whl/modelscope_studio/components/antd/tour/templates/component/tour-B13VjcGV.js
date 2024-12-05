import { g as ee, w as R } from "./Index-DCBEtshI.js";
const w = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tour;
var U = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, s) {
  var o, r = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) se.call(t, o) && !ce.hasOwnProperty(o) && (r[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
C.Fragment = oe;
C.jsx = H;
C.jsxs = H;
U.exports = C;
var g = U.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: L,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: E,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: he,
  init: me,
  insert_hydration: x,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: I,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Re
} = window.__gradio__svelte__internal;
function W(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), r = fe(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      r && r.l(l), l.forEach(E), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), r && r.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      r && r.p && (!s || l & /*$$scope*/
      64) && be(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? _e(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (I(r, e), s = !0);
    },
    o(e) {
      k(r, e), s = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, s, o, r, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = V("react-portal-target"), s = we(), e && e.c(), o = N(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(E), s = ue(l), e && e.l(l), o = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      x(l, t, a), n[8](t), x(l, s, a), e && e.m(l, a), x(l, o, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && I(e, 1)) : (e = W(l), e.c(), I(e, 1), e.m(o.parentNode, o)) : e && (he(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (I(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (E(t), E(s), E(o)), n[8](null), e && e.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Ie(n, t, s) {
  let o, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: c
  } = t;
  const p = R(D(t)), u = R();
  F(n, u, (d) => s(0, o = d));
  const f = R();
  F(n, f, (d) => s(1, r = d));
  const i = [], _ = ye("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: b
  } = ee() || {}, y = c({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(d) {
      i.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", y), Ee(() => {
    p.set(D(t));
  }), ve(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    s(17, t = T(T({}, t), A(d))), "svelteInit" in d && s(5, c = d.svelteInit), "$$scope" in d && s(6, l = d.$$scope);
  }, t = A(t), [o, r, u, f, a, c, l, e, v, K];
}
class Se extends ie {
  constructor(t) {
    super(), me(this, t, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(s) {
    const o = R(), r = new Se({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== o), M({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...s.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !Oe.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function j(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...w.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: a,
      useCapture: c
    }) => {
      s.addEventListener(a, l, c);
    });
  });
  const o = Array.from(n.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = j(e);
      t.push(...a), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const S = Q(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, r) => {
  const e = X(), [l, a] = Z([]);
  return $(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(r, i), s && i.classList.add(...s.split(" ")), o) {
        const _ = Pe(o);
        Object.keys(_).forEach((h) => {
          i.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var b, y, v;
        (b = e.current) != null && b.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: h,
          clonedElement: m
        } = j(n);
        return c = m, a(h), c.style.display = "contents", p(), (v = e.current) == null || v.appendChild(c), h.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", p(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var i, _;
      c.style.display = "", (i = e.current) != null && i.contains(c) && ((_ = e.current) == null || _.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, s, o, r]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n) {
  try {
    if (typeof n == "string") {
      let t = n.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function z(n) {
  return G(() => je(n), [n]);
}
function Y(n, t, s) {
  return n.filter(Boolean).map((o, r) => {
    var c;
    if (typeof o != "object")
      return o;
    const e = {
      ...o.props,
      key: ((c = o.props) == null ? void 0 : c.key) ?? (s ? `${s}-${r}` : `${r}`)
    };
    let l = e;
    Object.keys(o.slots).forEach((p) => {
      if (!o.slots[p] || !(o.slots[p] instanceof Element) && !o.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((m, b) => {
        l[m] || (l[m] = {}), b !== u.length - 1 && (l = e[m]);
      });
      const f = o.slots[p];
      let i, _, h = !1;
      f instanceof Element ? i = f : (i = f.el, _ = f.callback, h = f.clone ?? !1), l[u[u.length - 1]] = i ? _ ? (...m) => (_(u[u.length - 1], m), /* @__PURE__ */ g.jsx(S, {
        slot: i,
        clone: h
      })) : /* @__PURE__ */ g.jsx(S, {
        slot: i,
        clone: h
      }) : l[u[u.length - 1]], l = e;
    });
    const a = "children";
    return o[a] && (e[a] = Y(o[a], t, `${r}`)), e;
  });
}
function Te(n, t) {
  return n ? /* @__PURE__ */ g.jsx(S, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: t,
  slots: s
}, o) {
  return s[n] ? (...r) => (t(n, r), Te(s[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ne = Ce(({
  slots: n,
  steps: t,
  slotItems: s,
  children: o,
  onChange: r,
  onClose: e,
  getPopupContainer: l,
  setSlotParams: a,
  indicatorsRender: c,
  ...p
}) => {
  const u = z(l), f = z(c);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ g.jsx(te, {
      ...p,
      steps: G(() => t || Y(s), [t, s]),
      onChange: (i) => {
        r == null || r(i);
      },
      closeIcon: n.closeIcon ? /* @__PURE__ */ g.jsx(S, {
        slot: n.closeIcon
      }) : p.closeIcon,
      indicatorsRender: n.indicatorsRender ? Le({
        slots: n,
        setSlotParams: a,
        key: "indicatorsRender"
      }) : f,
      getPopupContainer: u,
      onClose: (i, ..._) => {
        e == null || e(i, ..._);
      }
    })]
  });
});
export {
  Ne as Tour,
  Ne as default
};
