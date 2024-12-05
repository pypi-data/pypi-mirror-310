import { c as compilerAssert, $, J as defineKit, K as Numeric, d as ignoreDiagnostics, L as CustomKeyMap } from './usage-resolver-DgwygYWr.js';
import { g as getEncode, a as getFormat, b as getVisibility, i as isIntrinsicType } from './decorators-D2z-p6Bs.js';
export { u as unsafe_useStateMap, c as unsafe_useStateSet } from './decorators-D2z-p6Bs.js';
import { a as createRekeyableMap } from './index-CbEjf-wE.js';
import './path-utils-3cuVtir1.js';

var _a;
class StateMapRealmView {
    #realm;
    #parentState;
    #realmState;
    constructor(realm, realmState, parentState) {
        this.#realm = realm;
        this.#parentState = parentState;
        this.#realmState = realmState;
    }
    has(t) {
        return this.dispatch(t).has(t) ?? false;
    }
    set(t, v) {
        this.dispatch(t).set(t, v);
        return this;
    }
    get(t) {
        return this.dispatch(t).get(t);
    }
    delete(t) {
        return this.dispatch(t).delete(t);
    }
    forEach(cb, thisArg) {
        for (const item of this.entries()) {
            cb.call(thisArg, item[1], item[0], this);
        }
        return this;
    }
    get size() {
        // extremely non-optimal, maybe worth not offering it?
        return [...this.entries()].length;
    }
    clear() {
        this.#realmState.clear();
    }
    *entries() {
        for (const item of this.#realmState) {
            yield item;
        }
        for (const item of this.#parentState) {
            yield item;
        }
        return undefined;
    }
    *values() {
        for (const item of this.entries()) {
            yield item[1];
        }
        return undefined;
    }
    *keys() {
        for (const item of this.entries()) {
            yield item[0];
        }
        return undefined;
    }
    [Symbol.iterator]() {
        return this.entries();
    }
    [Symbol.toStringTag] = "StateMap";
    dispatch(keyType) {
        if (this.#realm.hasType(keyType)) {
            return this.#realmState;
        }
        return this.#parentState;
    }
}
/** @experimental */
class Realm {
    #program;
    // Type registry
    /**
     * Stores all types owned by this realm.
     */
    #types = new Set();
    /**
     * Stores types that are deleted in this realm. When a realm is active and doing a traversal, you will
     * not find this type in e.g. collections. Deleted types are mapped to `null` if you ask for it.
     */
    #deletedTypes = new Set();
    #stateMaps = new Map();
    key;
    constructor(program, description) {
        this.key = Symbol(description);
        this.#program = program;
        _a.#knownRealms.set(this.key, this);
    }
    stateMap(stateKey) {
        let m = this.#stateMaps.get(stateKey);
        if (!m) {
            m = new Map();
            this.#stateMaps.set(stateKey, m);
        }
        return new StateMapRealmView(this, m, this.#program.stateMap(stateKey));
    }
    clone(type) {
        compilerAssert(type, "Undefined type passed to clone");
        const clone = this.#cloneIntoRealm(type);
        $.type.finishType(clone);
        return clone;
    }
    remove(type) {
        this.#deletedTypes.add(type);
    }
    hasType(type) {
        return this.#types.has(type);
    }
    addType(type) {
        this.#types.add(type);
        _a.realmForType.set(type, this);
    }
    #cloneIntoRealm(type) {
        const clone = $.type.clone(type);
        this.#types.add(clone);
        _a.realmForType.set(clone, this);
        return clone;
    }
    static #knownRealms = new Map();
    static realmForKey(key, parentRealm) {
        return this.#knownRealms.get(key);
    }
    static realmForType = new Map();
}
_a = Realm;

defineKit({
    literal: {
        create(value) {
            if (typeof value === "string") {
                return this.literal.createString(value);
            }
            else if (typeof value === "number") {
                return this.literal.createNumeric(value);
            }
            else {
                return this.literal.createBoolean(value);
            }
        },
        createString(value) {
            return this.program.checker.createType({
                kind: "String",
                value,
            });
        },
        createNumeric(value) {
            const valueAsString = String(value);
            return this.program.checker.createType({
                kind: "Number",
                value,
                valueAsString,
                numericValue: Numeric(valueAsString),
            });
        },
        createBoolean(value) {
            return this.program.checker.createType({
                kind: "Boolean",
                value,
            });
        },
        isBoolean(type) {
            return type.kind === "Boolean";
        },
        isString(type) {
            return type.kind === "String";
        },
        isNumeric(type) {
            return type.kind === "Number";
        },
        is(type) {
            return (this.literal.isBoolean(type) || this.literal.isNumeric(type) || this.literal.isString(type));
        },
    },
});

defineKit({
    modelProperty: {
        is(type) {
            return type.kind === "ModelProperty";
        },
        getEncoding(type) {
            return getEncode(this.program, type) ?? getEncode(this.program, type.type);
        },
        getFormat(type) {
            return getFormat(this.program, type) ?? getFormat(this.program, type.type);
        },
        getVisibility(property) {
            return getVisibility(this.program, property);
        },
    },
});

/** @experimental */
function copyMap(map) {
    return createRekeyableMap(Array.from(map.entries()));
}
/** @experimental */
function decoratorApplication(args) {
    if (!args) {
        return [];
    }
    const decorators = [];
    for (const arg of args) {
        decorators.push({
            decorator: Array.isArray(arg) ? arg[0] : arg,
            args: Array.isArray(arg)
                ? arg.slice(1).map((rawValue) => ({
                    value: typeof rawValue === "object" && rawValue !== null
                        ? rawValue
                        : $.literal.create(rawValue),
                    jsValue: rawValue,
                }))
                : [],
        });
    }
    return decorators;
}

defineKit({
    model: {
        create(desc) {
            const properties = createRekeyableMap(Array.from(Object.entries(desc.properties)));
            const model = this.program.checker.createType({
                kind: "Model",
                name: desc.name ?? "",
                decorators: decoratorApplication(desc.decorators),
                properties: properties,
                expression: desc.name === undefined,
                node: undefined,
                derivedModels: desc.derivedModels ?? [],
                sourceModels: desc.sourceModels ?? [],
            });
            this.program.checker.finishType(model);
            return model;
        },
        is(type) {
            return type.kind === "Model";
        },
    },
});

let _realm;
defineKit({
    realm: {
        get() {
            if (!_realm) {
                _realm = new Realm(this.program, " typekit realm");
            }
            return _realm;
        },
        set(realm) {
            _realm = realm;
        },
    },
});

defineKit({
    scalar: {
        is(type) {
            return type.kind === "Scalar";
        },
        extendsBoolean: extendsStdType("boolean"),
        extendsBytes: extendsStdType("bytes"),
        extendsDecimal: extendsStdType("decimal"),
        extendsDecimal128: extendsStdType("decimal128"),
        extendsDuration: extendsStdType("duration"),
        extendsFloat: extendsStdType("float"),
        extendsFloat32: extendsStdType("float32"),
        extendsFloat64: extendsStdType("float64"),
        extendsInt8: extendsStdType("int8"),
        extendsInt16: extendsStdType("int16"),
        extendsInt32: extendsStdType("int32"),
        extendsInt64: extendsStdType("int64"),
        extendsInteger: extendsStdType("integer"),
        extendsNumeric: extendsStdType("numeric"),
        extendsOffsetDateTime: extendsStdType("offsetDateTime"),
        extendsPlainDate: extendsStdType("plainDate"),
        extendsPlainTime: extendsStdType("plainTime"),
        extendsSafeint: extendsStdType("safeint"),
        extendsString: extendsStdType("string"),
        extendsUint8: extendsStdType("uint8"),
        extendsUint16: extendsStdType("uint16"),
        extendsUint32: extendsStdType("uint32"),
        extendsUint64: extendsStdType("uint64"),
        extendsUrl: extendsStdType("url"),
        extendsUtcDateTime: extendsStdType("utcDateTime"),
        isBoolean: isStdType("boolean"),
        isBytes: isStdType("bytes"),
        isDecimal: isStdType("decimal"),
        isDecimal128: isStdType("decimal128"),
        isDuration: isStdType("duration"),
        isFloat: isStdType("float"),
        isFloat32: isStdType("float32"),
        isFloat64: isStdType("float64"),
        isInt8: isStdType("int8"),
        isInt16: isStdType("int16"),
        isInt32: isStdType("int32"),
        isInt64: isStdType("int64"),
        isInteger: isStdType("integer"),
        isNumeric: isStdType("numeric"),
        isOffsetDateTime: isStdType("offsetDateTime"),
        isPlainDate: isStdType("plainDate"),
        isPlainTime: isStdType("plainTime"),
        isSafeint: isStdType("safeint"),
        isString: isStdType("string"),
        isUint8: isStdType("uint8"),
        isUint16: isStdType("uint16"),
        isUint32: isStdType("uint32"),
        isUint64: isStdType("uint64"),
        isUrl: isStdType("url"),
        isUtcDateTime: isStdType("utcDateTime"),
        getStdBase(type) {
            const tspNamespace = this.program.resolveTypeReference("TypeSpec")[0];
            let current = type;
            while (current) {
                if (current.namespace === tspNamespace) {
                    return current;
                }
                current = current.baseScalar;
            }
            return null;
        },
        getEncoding(type) {
            return getEncode(this.program, type);
        },
        getFormat(type) {
            return getFormat(this.program, type);
        },
    },
});
function isStdType(typeName) {
    return function (type) {
        return type === this.program.checker.getStdType(typeName);
    };
}
function extendsStdType(typeName) {
    return function (type) {
        if (!this.scalar.is(type)) {
            return false;
        }
        return isIntrinsicType(this.program, type, typeName);
    };
}

defineKit({
    type: {
        finishType(type) {
            this.program.checker.finishType(type);
        },
        clone(type) {
            let clone;
            switch (type.kind) {
                case "Model":
                    clone = this.program.checker.createType({
                        ...type,
                        decorators: [...type.decorators],
                        properties: copyMap(type.properties),
                        indexer: type.indexer ? { ...type.indexer } : undefined,
                    });
                    break;
                case "Union":
                    clone = this.program.checker.createType({
                        ...type,
                        decorators: [...type.decorators],
                        variants: copyMap(type.variants),
                        get options() {
                            return Array.from(this.variants.values()).map((v) => v.type);
                        },
                    });
                    break;
                case "Interface":
                    clone = this.program.checker.createType({
                        ...type,
                        decorators: [...type.decorators],
                        operations: copyMap(type.operations),
                    });
                    break;
                case "Enum":
                    clone = this.program.checker.createType({
                        ...type,
                        members: copyMap(type.members),
                    });
                    break;
                case "Namespace":
                    clone = this.program.checker.createType({
                        ...type,
                        decorators: [...type.decorators],
                        decoratorDeclarations: new Map(type.decoratorDeclarations),
                        models: new Map(type.models),
                        enums: new Map(type.enums),
                        functionDeclarations: new Map(type.functionDeclarations),
                        instantiationParameters: type.instantiationParameters
                            ? [...type.instantiationParameters]
                            : undefined,
                        interfaces: new Map(type.interfaces),
                        namespaces: new Map(type.namespaces),
                        operations: new Map(type.operations),
                        projections: [...type.projections],
                        scalars: new Map(type.scalars),
                        unions: new Map(type.unions),
                    });
                    break;
                default:
                    clone = this.program.checker.createType({
                        ...type,
                        ...("decorators" in type ? { decorators: [...type.decorators] } : {}),
                    });
                    break;
            }
            this.realm.get().addType(clone);
            return clone;
        },
    },
});

defineKit({
    unionVariant: {
        create(desc) {
            const variant = this.program.checker.createType({
                kind: "UnionVariant",
                name: desc.name ?? Symbol("name"),
                decorators: decoratorApplication(desc.decorators),
                type: desc.type,
                node: undefined,
                union: desc.union,
            });
            this.program.checker.finishType(variant);
            return variant;
        },
        is(type) {
            return type.kind === "UnionVariant";
        },
    },
});

defineKit({
    union: {
        create(desc) {
            const union = this.program.checker.createType({
                kind: "Union",
                name: desc.name,
                decorators: decoratorApplication(desc.decorators),
                variants: createRekeyableMap(),
                get options() {
                    return Array.from(this.variants.values()).map((v) => v.type);
                },
                expression: desc.name === undefined,
                node: undefined,
            });
            if (Array.isArray(desc.variants)) {
                for (const variant of desc.variants) {
                    union.variants.set(variant.name, variant);
                    variant.union = union;
                }
            }
            else if (desc.variants) {
                for (const [name, value] of Object.entries(desc.variants)) {
                    union.variants.set(name, this.unionVariant.create({ name, type: this.literal.create(value) }));
                }
            }
            this.program.checker.finishType(union);
            return union;
        },
        is(type) {
            return type.kind === "Union";
        },
        isValidEnum(type) {
            for (const variant of type.variants.values()) {
                if (!this.literal.isString(variant.type) && !this.literal.isNumeric(variant.type)) {
                    return false;
                }
            }
            return true;
        },
        isExtensible(type) {
            const variants = Array.from(type.variants.values());
            if (variants.length === 0) {
                return false;
            }
            for (let i = 0; i < variants.length; i++) {
                let isCommon = true;
                for (let j = 0; j < variants.length; j++) {
                    if (i === j) {
                        continue;
                    }
                    const assignable = ignoreDiagnostics(this.program.checker.isTypeAssignableTo(variants[j].type, variants[i].type, type));
                    if (!assignable) {
                        isCommon = false;
                        break;
                    }
                }
                if (isCommon) {
                    return true;
                }
            }
            return false;
        },
    },
});

/** @experimental */
var MutatorFlow;
(function (MutatorFlow) {
    MutatorFlow[MutatorFlow["MutateAndRecurse"] = 0] = "MutateAndRecurse";
    MutatorFlow[MutatorFlow["DoNotMutate"] = 1] = "DoNotMutate";
    MutatorFlow[MutatorFlow["DoNotRecurse"] = 2] = "DoNotRecurse";
})(MutatorFlow || (MutatorFlow = {}));
const typeId = CustomKeyMap.objectKeyer();
const mutatorId = CustomKeyMap.objectKeyer();
const seen = new CustomKeyMap(([type, mutators]) => {
    const key = `${typeId.getKey(type)}-${[...mutators.values()]
        .map((v) => mutatorId.getKey(v))
        .join("-")}`;
    return key;
});
/** @experimental */
function mutateSubgraph(program, mutators, type) {
    const realm = new Realm(program, "realm for mutation");
    const interstitialFunctions = [];
    const mutated = mutateSubgraphWorker(type, new Set(mutators));
    if (mutated === type) {
        return { realm: null, type };
    }
    else {
        return { realm, type: mutated };
    }
    function mutateSubgraphWorker(type, activeMutators) {
        let existing = seen.get([type, activeMutators]);
        if (existing) {
            clearInterstitialFunctions();
            return existing;
        }
        let clone = null;
        const mutatorsWithOptions = [];
        // step 1: see what mutators to run
        const newMutators = new Set(activeMutators.values());
        for (const mutator of activeMutators) {
            const record = mutator[type.kind];
            if (!record) {
                continue;
            }
            let mutationFn = null;
            let replaceFn = null;
            let mutate = false;
            let recurse = false;
            if (typeof record === "function") {
                mutationFn = record;
                mutate = true;
                recurse = true;
            }
            else {
                mutationFn = "mutate" in record ? record.mutate : null;
                replaceFn = "replace" in record ? record.replace : null;
                if (record.filter) {
                    const filterResult = record.filter(type, program, realm);
                    if (filterResult === true) {
                        mutate = true;
                        recurse = true;
                    }
                    else if (filterResult === false) {
                        mutate = false;
                        recurse = true;
                    }
                    else {
                        mutate = (filterResult & MutatorFlow.DoNotMutate) === 0;
                        recurse = (filterResult & MutatorFlow.DoNotRecurse) === 0;
                    }
                }
                else {
                    mutate = true;
                    recurse = true;
                }
            }
            if (!recurse) {
                newMutators.delete(mutator);
            }
            if (mutate) {
                mutatorsWithOptions.push({ mutator, mutationFn, replaceFn });
            }
        }
        const mutatorsToApply = mutatorsWithOptions.map((v) => v.mutator);
        // if we have no mutators to apply, let's bail out.
        if (mutatorsWithOptions.length === 0) {
            if (newMutators.size > 0) {
                // we might need to clone this type later if something in our subgraph needs mutated.
                interstitialFunctions.push(initializeClone);
                visitSubgraph();
                interstitialFunctions.pop();
                return clone ?? type;
            }
            else {
                // we don't need to clone this type, so let's just return it.
                return type;
            }
        }
        // step 2: see if we need to mutate based on the set of mutators we're actually going to run
        existing = seen.get([type, mutatorsToApply]);
        if (existing) {
            clearInterstitialFunctions();
            return existing;
        }
        // step 3: run the mutators
        clearInterstitialFunctions();
        initializeClone();
        for (const { mutationFn, replaceFn } of mutatorsWithOptions) {
            // todo: handle replace earlier in the mutation chain
            const result = (mutationFn ?? replaceFn)(type, clone, program, realm);
            if (replaceFn && result !== undefined) {
                clone = result;
                seen.set([type, activeMutators], clone);
                seen.set([type, mutatorsToApply], clone);
            }
        }
        if (newMutators.size > 0) {
            visitSubgraph();
        }
        $.type.finishType(clone);
        return clone;
        function initializeClone() {
            clone = $.type.clone(type);
            seen.set([type, activeMutators], clone);
            seen.set([type, mutatorsToApply], clone);
        }
        function clearInterstitialFunctions() {
            for (const interstitial of interstitialFunctions) {
                interstitial();
            }
            interstitialFunctions.length = 0;
        }
        function visitSubgraph() {
            const root = clone ?? type;
            switch (root.kind) {
                case "Model":
                    for (const prop of root.properties.values()) {
                        const newProp = mutateSubgraphWorker(prop, newMutators);
                        if (clone) {
                            clone.properties.set(prop.name, newProp);
                        }
                    }
                    if (root.indexer) {
                        const res = mutateSubgraphWorker(root.indexer.value, newMutators);
                        if (clone) {
                            clone.indexer.value = res;
                        }
                    }
                    break;
                case "ModelProperty":
                    const newType = mutateSubgraphWorker(root.type, newMutators);
                    if (clone) {
                        clone.type = newType;
                    }
                    break;
                case "Operation":
                    const newParams = mutateSubgraphWorker(root.parameters, newMutators);
                    if (clone) {
                        clone.parameters = newParams;
                    }
                    break;
                case "Scalar":
                    const newBaseScalar = root.baseScalar
                        ? mutateSubgraphWorker(root.baseScalar, newMutators)
                        : undefined;
                    if (clone) {
                        clone.baseScalar = newBaseScalar;
                    }
            }
        }
    }
}

export { $ as unsafe_$, MutatorFlow as unsafe_MutatorFlow, Realm as unsafe_Realm, mutateSubgraph as unsafe_mutateSubgraph };
