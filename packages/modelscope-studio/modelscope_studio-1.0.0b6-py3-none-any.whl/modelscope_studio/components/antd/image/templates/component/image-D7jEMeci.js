import { g as ee, w as E } from "./Index-CdWZ5MgO.js";
const _ = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Image;
var G = {
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
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, t, o) {
  var l, r = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) le.call(t, l) && !ie.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: re,
    type: e,
    key: n,
    ref: s,
    props: r,
    _owner: se.current
  };
}
x.Fragment = oe;
x.jsx = H;
x.jsxs = H;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: F,
  check_outros: ae,
  children: K,
  claim_element: q,
  claim_space: de,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: fe,
  detach: h,
  element: V,
  empty: A,
  exclude_internal_props: W,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: _e,
  init: he,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: we,
  transition_in: C,
  transition_out: j,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: ye,
  onDestroy: Ee,
  setContext: Re
} = window.__gradio__svelte__internal;
function D(e) {
  let t, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = q(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      R(n, t, s), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && be(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? me(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (C(r, n), o = !0);
    },
    o(n) {
      j(r, n), o = !1;
    },
    d(n) {
      n && h(t), r && r.d(n), e[9](null);
    }
  };
}
function Ce(e) {
  let t, o, l, r, n = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      t = V("react-portal-target"), o = we(), n && n.c(), l = A(), this.h();
    },
    l(s) {
      t = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(h), o = de(s), n && n.l(s), l = A(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, t, c), e[8](t), R(s, o, c), n && n.m(s, c), R(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && C(n, 1)) : (n = D(s), n.c(), C(n, 1), n.m(l.parentNode, l)) : n && (_e(), j(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(s) {
      r || (C(n), r = !0);
    },
    o(s) {
      j(n), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), e[8](null), n && n.d(s);
    }
  };
}
function M(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function Ie(e, t, o) {
  let l, r, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = ue(n);
  let {
    svelteInit: i
  } = t;
  const g = E(M(t)), u = E();
  N(e, u, (a) => o(0, l = a));
  const m = E();
  N(e, m, (a) => o(1, r = a));
  const d = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: S,
    subSlotIndex: b
  } = ee() || {}, v = i({
    parent: f,
    props: g,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: S,
    subSlotIndex: b,
    onDestroy(a) {
      d.push(a);
    }
  });
  Re("$$ms-gr-react-wrapper", v), ve(() => {
    g.set(M(t));
  }), Ee(() => {
    d.forEach((a) => a());
  });
  function y(a) {
    F[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  function J(a) {
    F[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, t = T(T({}, t), W(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = W(t), [l, r, u, m, c, i, s, n, y, J];
}
class xe extends ce {
  constructor(t) {
    super(), he(this, t, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, k = window.ms_globals.tree;
function Se(e) {
  function t(o) {
    const l = E(), r = new xe({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? k;
          return c.nodes = [...c.nodes, s], U({
            createPortal: P,
            node: k
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: P,
              node: k
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
      o(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return typeof l == "number" && !ke.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function L(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(_.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: _.Children.toArray(e._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: s,
            children: [..._.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = L(n);
      t.push(...c), o.appendChild(s);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Pe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const I = Y(({
  slot: e,
  clone: t,
  className: o,
  style: l
}, r) => {
  const n = Q(), [s, c] = X([]);
  return Z(() => {
    var m;
    if (!n.current || !e)
      return;
    let i = e;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Pe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const f = Oe(l);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b, v, y;
        (b = n.current) != null && b.contains(i) && ((v = n.current) == null || v.removeChild(i));
        const {
          portals: p,
          clonedElement: S
        } = L(e);
        return i = S, c(p), i.style.display = "contents", g(), (y = n.current) == null || y.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(e, {
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
  }, [e, t, o, l, r]), _.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(e) {
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
function O(e) {
  return $(() => je(e), [e]);
}
function Le(e) {
  return Object.keys(e).reduce((t, o) => (e[o] !== void 0 && (t[o] = e[o]), t), {});
}
function Te(e, t) {
  return e ? /* @__PURE__ */ w.jsx(I, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function z({
  key: e,
  setSlotParams: t,
  slots: o
}, l) {
  return o[e] ? (...r) => (t(e, r), Te(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function Fe(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Ae = Se(({
  slots: e,
  preview: t,
  setSlotParams: o,
  ...l
}) => {
  const r = Fe(t), n = e["preview.mask"] || e["preview.closeIcon"] || e["preview.toolbarRender"] || e["preview.imageRender"] || t !== !1, s = O(r.getContainer), c = O(r.toolbarRender), i = O(r.imageRender);
  return /* @__PURE__ */ w.jsx(te, {
    ...l,
    preview: n ? Le({
      ...r,
      getContainer: s,
      toolbarRender: e["preview.toolbarRender"] ? z({
        slots: e,
        setSlotParams: o,
        key: "preview.toolbarRender"
      }) : c,
      imageRender: e["preview.imageRender"] ? z({
        slots: e,
        setSlotParams: o,
        key: "preview.imageRender"
      }) : i,
      ...e["preview.mask"] || Reflect.has(r, "mask") ? {
        mask: e["preview.mask"] ? /* @__PURE__ */ w.jsx(I, {
          slot: e["preview.mask"]
        }) : r.mask
      } : {},
      closeIcon: e["preview.closeIcon"] ? /* @__PURE__ */ w.jsx(I, {
        slot: e["preview.closeIcon"]
      }) : r.closeIcon
    }) : !1,
    placeholder: e.placeholder ? /* @__PURE__ */ w.jsx(I, {
      slot: e.placeholder
    }) : l.placeholder
  });
});
export {
  Ae as Image,
  Ae as default
};
