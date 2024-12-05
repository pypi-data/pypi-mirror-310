import { g as Z, w as y } from "./Index-B7wzqvzl.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, x = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Image;
var M = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, s) {
  var o, r = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) re.call(t, o) && !se.hasOwnProperty(o) && (r[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: oe.current
  };
}
I.Fragment = ne;
I.jsx = z;
I.jsxs = z;
M.exports = I;
var k = M.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: K,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: q,
  space: he,
  transition_in: C,
  transition_out: P,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), r = ue(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, t, l), r && r.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      r && r.p && (!s || l & /*$$scope*/
      64) && ge(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (C(r, e), s = !0);
    },
    o(e) {
      P(r, e), s = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, s, o, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = K("react-portal-target"), s = he(), e && e.c(), o = N(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), s = ce(l), e && e.l(l), o = N(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, t, c), n[8](t), E(l, s, c), e && e.m(l, c), E(l, o, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = F(l), e.c(), C(e, 1), e.m(o.parentNode, o)) : e && (pe(), P(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (C(e), r = !0);
    },
    o(l) {
      P(e), r = !1;
    },
    d(l) {
      l && (h(t), h(s), h(o)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Ce(n, t, s) {
  let o, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = y(W(t)), d = y();
  j(n, d, (a) => s(0, o = a));
  const _ = y();
  j(n, _, (a) => s(1, r = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w
  } = Z() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", b), we(() => {
    g.set(W(t));
  }), ve(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    T[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  function V(a) {
    T[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  return n.$$set = (a) => {
    s(17, t = L(L({}, t), A(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, l = a.$$scope);
  }, t = A(t), [o, r, d, _, c, i, l, e, v, V];
}
class Ie extends le {
  constructor(t) {
    super(), _e(this, t, Ce, Ee, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function t(s) {
    const o = y(), r = new Ie({
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, l], D({
            createPortal: x,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), D({
              createPortal: x,
              node: S
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
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !ke.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function O(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(x(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...m.Children.toArray(r.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      t.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const G = B(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), xe(r, u), s && u.classList.add(...s.split(" ")), o) {
        const f = Se(o);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w, b, v;
        (w = e.current) != null && w.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = O(n);
        return i = R, c(p), i.style.display = "contents", g(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, s, o, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(n) {
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
function Oe(n) {
  return X(() => Pe(n), [n]);
}
function Le(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const je = Re(({
  slots: n,
  preview: t,
  ...s
}) => {
  const o = Le(t), r = n["preview.mask"] || n["preview.closeIcon"] || t !== !1, e = Oe(o.getContainer);
  return /* @__PURE__ */ k.jsx($.PreviewGroup, {
    ...s,
    preview: r ? {
      ...o,
      getContainer: e,
      ...n["preview.mask"] || Reflect.has(o, "mask") ? {
        mask: n["preview.mask"] ? /* @__PURE__ */ k.jsx(G, {
          slot: n["preview.mask"]
        }) : o.mask
      } : {},
      closeIcon: n["preview.closeIcon"] ? /* @__PURE__ */ k.jsx(G, {
        slot: n["preview.closeIcon"]
      }) : o.closeIcon
    } : !1
  });
});
export {
  je as ImagePreviewGroup,
  je as default
};
