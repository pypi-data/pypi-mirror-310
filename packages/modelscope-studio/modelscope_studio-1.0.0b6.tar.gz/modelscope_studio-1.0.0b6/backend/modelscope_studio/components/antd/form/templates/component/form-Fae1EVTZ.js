import { g as $, w as E } from "./Index-BiKEiWBr.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, P = window.ms_globals.antd.Form;
var G = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) re.call(e, s) && !se.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: te,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: oe.current
  };
}
C.Fragment = ne;
C.jsx = U;
C.jsxs = U;
G.exports = C;
var q = G.exports;
const {
  SvelteComponent: le,
  assign: F,
  binding_callbacks: L,
  check_outros: ie,
  children: H,
  claim_element: K,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: B,
  empty: N,
  exclude_internal_props: j,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: J,
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
function A(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = B("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(e);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      v(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? fe(
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
      r || (S(o, t), r = !0);
    },
    o(t) {
      k(o, t), r = !1;
    },
    d(t) {
      t && g(e), o && o.d(t), n[9](null);
    }
  };
}
function ve(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      e = B("react-portal-target"), r = he(), t && t.c(), s = N(), this.h();
    },
    l(l) {
      e = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(e).forEach(g), r = ce(l), t && t.l(l), s = N(), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, e, c), n[8](e), v(l, r, c), t && t.m(l, c), v(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = A(l), t.c(), S(t, 1), t.m(s.parentNode, s)) : t && (_e(), k(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(l) {
      o || (S(t), o = !0);
    },
    o(l) {
      k(t), o = !1;
    },
    d(l) {
      l && (g(e), g(r), g(s)), n[8](null), t && t.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Se(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ae(t);
  let {
    svelteInit: i
  } = e;
  const m = E(W(e)), d = E();
  T(n, d, (u) => r(0, s = u));
  const f = E();
  T(n, f, (u) => r(1, o = u));
  const a = [], _ = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w
  } = $() || {}, b = i({
    parent: _,
    props: m,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), we(() => {
    m.set(W(e));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function y(u) {
    L[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function V(u) {
    L[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, e = F(F({}, e), j(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, e = j(e), [s, o, d, f, c, i, l, t, y, V];
}
class Ce extends le {
  constructor(e) {
    super(), pe(this, e, Se, ve, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function e(r) {
    const s = E(), o = new Ce({
      ...r,
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
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, l], D({
            createPortal: x,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: x,
              node: I
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
function Ie(n) {
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
function M(n) {
  return Y(() => Ie(n), [n]);
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !xe.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function O(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(x(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = O(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(t);
      e.push(...c), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const Pe = Q(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = X(), [l, c] = Z([]);
  return z(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var w, b, y;
        (w = t.current) != null && w.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = O(n);
        return i = R, c(p), i.style.display = "contents", m(), (y = t.current) == null || y.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, r, s, o]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Fe(n, e) {
  return n ? /* @__PURE__ */ q.jsx(Pe, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...o) => (e(n, o), Fe(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Re(({
  value: n,
  onValueChange: e,
  requiredMark: r,
  onValuesChange: s,
  feedbackIcons: o,
  setSlotParams: t,
  slots: l,
  ...c
}) => {
  const [i] = P.useForm(), m = M(o), d = M(r);
  return z(() => {
    i.setFieldsValue(n);
  }, [i, n]), /* @__PURE__ */ q.jsx(P, {
    ...c,
    initialValues: n,
    form: i,
    requiredMark: l.requiredMark ? Le({
      key: "requiredMark",
      setSlotParams: t,
      slots: l
    }) : r === "optional" ? r : d || r,
    feedbackIcons: m,
    onValuesChange: (f, a) => {
      e(a), s == null || s(f, a);
    }
  });
});
export {
  Ne as Form,
  Ne as default
};
