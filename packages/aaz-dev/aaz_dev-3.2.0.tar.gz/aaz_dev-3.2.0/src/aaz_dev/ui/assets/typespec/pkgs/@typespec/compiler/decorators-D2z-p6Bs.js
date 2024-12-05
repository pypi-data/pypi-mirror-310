import { d as ignoreDiagnostics, g as getTypeName, c as compilerAssert, s as setDocData, e as getDocDataInternal, f as reportDeprecated, h as getMaxLengthAsNumeric, j as setMinLength, k as getMinLengthAsNumeric, l as setMaxLength, m as isArrayModelType, n as getMaxItemsAsNumeric, o as setMinItems, p as getMinItemsAsNumeric, q as setMaxItems, t as getMaxValueAsNumeric, u as getMaxValueExclusiveAsNumeric, v as setMinValue, w as getMinValueAsNumeric, x as getMinValueExclusiveAsNumeric, y as setMaxValue, z as setMinValueExclusive, A as setMaxValueExclusive, B as isValue, F as markDeprecated, G as getDeprecationDetails, H as getDiscriminatedUnion, I as setDiscriminator } from './usage-resolver-DgwygYWr.js';
import { r as reportDiagnostic, c as createDiagnostic, S as SyntaxKind } from './index-CbEjf-wE.js';

/**
 * Validate the decorator target is matching the expected value.
 * @param context
 * @param target
 * @param decoratorName
 * @param expectedType
 * @returns
 */
function validateDecoratorTarget(context, target, decoratorName, expectedType) {
    const isCorrectType = isTypeSpecValueTypeOf(target, expectedType);
    if (!isCorrectType) {
        reportDiagnostic(context.program, {
            code: "decorator-wrong-target",
            format: {
                decorator: decoratorName,
                to: target.kind,
            },
            target: context.decoratorTarget,
        });
        return false;
    }
    return true;
}
function isIntrinsicType(program, type, kind) {
    return ignoreDiagnostics(program.checker.isTypeAssignableTo(type.projectionBase ?? type, program.checker.getStdType(kind), type));
}
/**
 * @deprecated this function is deprecated use decorator definition in TypeSpec instead or check assignability directly.
 */
function validateDecoratorTargetIntrinsic(context, target, decoratorName, expectedType) {
    const expectedTypeStrs = typeof expectedType === "string" ? [expectedType] : expectedType;
    const expectedTypes = expectedTypeStrs.map((x) => context.program.checker.getStdType(x));
    const type = getPropertyType(target);
    const isCorrect = expectedTypes.some((x) => context.program.checker.isTypeAssignableTo(type, x, type)[0]);
    if (!isCorrect) {
        context.program.reportDiagnostic(createDiagnostic({
            code: "decorator-wrong-target",
            format: {
                decorator: decoratorName,
                to: `type it is not one of: ${expectedTypeStrs.join(", ")}`,
            },
            target: context.decoratorTarget,
        }));
        return false;
    }
    return true;
}
/** @deprecated use isTypeSpecValueTypeOf */
const isCadlValueTypeOf = isTypeSpecValueTypeOf;
/**
 * Check if the given target is of any of the TypeSpec types.
 * @param target Target to validate.
 * @param expectedType One or multiple allowed TypeSpec types.
 * @returns boolean if the target is of one of the allowed types.
 */
function isTypeSpecValueTypeOf(target, expectedType) {
    const kind = getTypeKind(target);
    if (kind === undefined) {
        return false;
    }
    return typeof expectedType === "string"
        ? expectedType === "Any" || kind === expectedType
        : expectedType.includes("Any") || expectedType.includes(kind);
}
function getTypeKind(target) {
    switch (typeof target) {
        case "object":
            return target.kind;
        case "string":
            return "String";
        case "number":
            return "Number";
        case "boolean":
            return "Boolean";
        default:
            return undefined;
    }
}
/**
 * Validate a decorator parameter has the correct type.
 * @param program Program
 * @param target Decorator target
 * @param value Value of the parameter.
 * @param expectedType Expected type or list of expected type
 * @returns true if the value is of one of the type in the list of expected types. If not emit a diagnostic.
 * @deprecated use @see createDecoratorDefinition#validate instead.
 */
function validateDecoratorParamType(program, target, value, expectedType) {
    if (!isTypeSpecValueTypeOf(value, expectedType)) {
        reportDiagnostic(program, {
            code: "invalid-argument",
            format: {
                value: prettyValue(program, value),
                expected: typeof expectedType === "string" ? expectedType : expectedType.join(", "),
            },
            target,
        });
        return false;
    }
    return true;
}
/**
 * @deprecated use extern dec definition in TypeSpec instead.
 */
function createDecoratorDefinition(definition) {
    const minParams = definition.args.filter((x) => !x.optional).length;
    const maxParams = definition.spreadArgs ? undefined : definition.args.length;
    function validate(context, target, args) {
        if (!validateDecoratorTarget(context, target, definition.name, definition.target) ||
            !validateDecoratorParamCount(context, minParams, maxParams, args)) {
            return false;
        }
        for (const [index, arg] of args.entries()) {
            const paramDefinition = definition.args[index] ?? definition.spreadArgs;
            if (arg === undefined) {
                if (!paramDefinition.optional) {
                    reportDiagnostic(context.program, {
                        code: "invalid-argument",
                        format: {
                            value: "undefined",
                            expected: expectedTypeList(paramDefinition.kind),
                        },
                        target: context.getArgumentTarget(index),
                    });
                    return false;
                }
            }
            else if (!isTypeSpecValueTypeOf(arg, paramDefinition.kind)) {
                reportDiagnostic(context.program, {
                    code: "invalid-argument",
                    format: {
                        value: prettyValue(context.program, arg),
                        expected: expectedTypeList(paramDefinition.kind),
                    },
                    target: context.getArgumentTarget(index),
                });
                return false;
            }
        }
        return true;
    }
    return {
        validate(context, target, parameters) {
            return validate(context, target, parameters);
        },
    };
}
function expectedTypeList(expectedType) {
    return typeof expectedType === "string" ? expectedType : expectedType.join(", ");
}
function validateDecoratorParamCount(context, min, max, parameters) {
    let missing = 0;
    for (let i = parameters.length - 1; i >= 0; i--) {
        if (parameters[i] === undefined) {
            missing++;
        }
        else {
            break;
        }
    }
    const parameterCount = parameters.length - missing;
    if (parameterCount < min || (max !== undefined && parameterCount > max)) {
        if (min === max) {
            reportDiagnostic(context.program, {
                code: "invalid-argument-count",
                format: {
                    actual: parameterCount.toString(),
                    expected: min.toString(),
                },
                target: context.decoratorTarget,
            });
        }
        else {
            reportDiagnostic(context.program, {
                code: "invalid-argument-count",
                format: {
                    actual: parameterCount.toString(),
                    expected: `${min}-${max === undefined ? "infinity" : max.toString()}`,
                },
                target: context.decoratorTarget,
            });
        }
        return false;
    }
    return true;
}
function prettyValue(program, value) {
    if (typeof value === "object" && value !== null && "kind" in value) {
        return getTypeName(value);
    }
    return value;
}
/** @deprecated use typespecTypeToJson */
const cadlTypeToJson = typespecTypeToJson;
/**
 * Convert a TypeSpec type to a serializable Json object.
 * Emits diagnostics if the given type is invalid
 * @param typespecType The type to convert to Json data
 * @param target The diagnostic target in case of errors.
 */
function typespecTypeToJson(typespecType, target) {
    if (typeof typespecType !== "object") {
        return [typespecType, []];
    }
    return typespecTypeToJsonInternal(typespecType, target, []);
}
function typespecTypeToJsonInternal(typespecType, target, path) {
    switch (typespecType.kind) {
        case "String":
        case "Boolean":
        case "Number":
            return [typespecType.value, []];
        case "EnumMember":
            return [typespecType.value ?? typespecType.name, []];
        case "Tuple": {
            const result = [];
            for (const [index, type] of typespecType.values.entries()) {
                const [item, diagnostics] = typespecTypeToJsonInternal(type, target, [
                    ...path,
                    index.toString(),
                ]);
                if (diagnostics.length > 0) {
                    return [undefined, diagnostics];
                }
                result.push(item);
            }
            return [result, []];
        }
        case "Model": {
            const result = {};
            for (const [name, type] of typespecType.properties.entries()) {
                const [item, diagnostics] = typespecTypeToJsonInternal(type.type, target, [
                    ...path,
                    name.toString(),
                ]);
                if (diagnostics.length > 0) {
                    return [undefined, diagnostics];
                }
                result[name] = item;
            }
            return [result, []];
        }
        default:
            const diagnostic = path.length === 0
                ? createDiagnostic({
                    code: "invalid-value",
                    format: {
                        kind: typespecType.kind,
                    },
                    target,
                })
                : createDiagnostic({
                    code: "invalid-value",
                    messageId: "atPath",
                    format: {
                        kind: typespecType.kind,
                        path: path.join("."),
                    },
                    target,
                });
            return [undefined, [diagnostic]];
    }
}
function validateDecoratorUniqueOnNode(context, type, decorator) {
    compilerAssert("decorators" in type, "Type should have decorators");
    const sameDecorators = type.decorators.filter((x) => x.decorator === decorator &&
        x.node?.kind === SyntaxKind.DecoratorExpression &&
        x.node?.parent === type.node);
    if (sameDecorators.length > 1) {
        reportDiagnostic(context.program, {
            code: "duplicate-decorator",
            format: { decoratorName: "@" + decorator.name.slice(1) },
            target: context.decoratorTarget,
        });
        return false;
    }
    return true;
}
/**
 * Validate that a given decorator is not on a type or any of its base types.
 * Useful to check for decorator usage that conflicts with another decorator.
 * @param context Decorator context
 * @param type The type to check
 * @param badDecorator The decorator we don't want present
 * @param givenDecorator The decorator that is the reason why we don't want the bad decorator present
 * @param includeHeritage Whether to check base types for the bad decorator too
 * @returns Whether the decorator application is valid
 */
function validateDecoratorNotOnType(context, type, badDecorator, givenDecorator) {
    compilerAssert("decorators" in type, "Type should have decorators");
    const decAppsToCheck = [];
    let base = type;
    while (base) {
        decAppsToCheck.push(...base.decorators);
        base = getHeritage(base);
    }
    for (const decapp of decAppsToCheck) {
        if (decapp.decorator === badDecorator) {
            reportDiagnostic(context.program, {
                code: "decorator-conflict",
                format: {
                    decoratorName: "@" + badDecorator.name.slice(1),
                    otherDecoratorName: "@" + givenDecorator.name.slice(1),
                },
                target: context.decoratorTarget,
            });
            return false;
        }
    }
    return true;
    function getHeritage(type) {
        if (type.kind === "Model") {
            return type.baseModel;
        }
        else if (type.kind === "Scalar") {
            return type.baseScalar;
        }
        else {
            return undefined;
        }
    }
}
/**
 * Return the type of the property or the model itself.
 */
function getPropertyType(target) {
    if (target.kind === "ModelProperty") {
        return target.type;
    }
    else {
        return target;
    }
}

/** @experimental */
function unsafe_useStateMap(key) {
    const getter = (program, target) => program.stateMap(key).get(target);
    const setter = (program, target, value) => program.stateMap(key).set(target, value);
    const mapGetter = (program) => program.stateMap(key);
    return [getter, setter, mapGetter];
}
/** @experimental */
function unsafe_useStateSet(key) {
    const getter = (program, target) => program.stateSet(key).has(target);
    const setter = (program, target) => program.stateSet(key).add(target);
    return [getter, setter];
}

function createStateSymbol$1(name) {
    return Symbol.for(`TypeSpec.${name}`);
}
function useStateMap(key) {
    return unsafe_useStateMap(typeof key === "string" ? createStateSymbol$1(key) : key);
}
function useStateSet(key) {
    return unsafe_useStateSet(typeof key === "string" ? createStateSymbol$1(key) : key);
}

const namespace = "TypeSpec";
function replaceTemplatedStringFromProperties(formatString, sourceObject) {
    // Template parameters are not valid source objects, just skip them
    if (sourceObject.kind === "TemplateParameter") {
        return formatString;
    }
    return formatString.replace(/{(\w+)}/g, (_, propName) => {
        return sourceObject[propName];
    });
}
function createStateSymbol(name) {
    return Symbol.for(`TypeSpec.${name}`);
}
const [getSummary, setSummary] = useStateMap("summary");
/**
 * @summary attaches a documentation string. It is typically used to give a short, single-line
 * description, and can be used in combination with or instead of @doc.
 *
 * The first argument to @summary is a string, which may contain template parameters, enclosed in braces,
 * which are replaced with an attribute for the type (commonly "name") passed as the second (optional) argument.
 *
 * @summary can be specified on any language element -- a model, an operation, a namespace, etc.
 */
const $summary = (context, target, text, sourceObject) => {
    if (sourceObject) {
        text = replaceTemplatedStringFromProperties(text, sourceObject);
    }
    setSummary(context.program, target, text);
};
/**
 * @doc attaches a documentation string. Works great with multi-line string literals.
 *
 * The first argument to @doc is a string, which may contain template parameters, enclosed in braces,
 * which are replaced with an attribute for the type (commonly "name") passed as the second (optional) argument.
 *
 * @doc can be specified on any language element -- a model, an operation, a namespace, etc.
 */
const $doc = (context, target, text, sourceObject) => {
    validateDecoratorUniqueOnNode(context, target, $doc);
    if (sourceObject) {
        text = replaceTemplatedStringFromProperties(text, sourceObject);
    }
    setDocData(context.program, target, "self", { value: text, source: "decorator" });
};
/**
 * Get the documentation string for the given type.
 * @param program Program
 * @param target Type
 * @returns Documentation value
 */
function getDoc(program, target) {
    return getDocDataInternal(program, target, "self")?.value;
}
const $returnsDoc = (context, target, text) => {
    validateDecoratorUniqueOnNode(context, target, $doc);
    setDocData(context.program, target, "returns", { value: text, source: "decorator" });
};
/**
 * Get the documentation information for the return success types of an operation. In most cases you probably just want to use {@link getReturnsDoc}
 * @param program Program
 * @param target Type
 * @returns Doc data with source information.
 */
function getReturnsDocData(program, target) {
    return getDocDataInternal(program, target, "returns");
}
/**
 * Get the documentation string for the return success types of an operation.
 * @param program Program
 * @param target Type
 * @returns Documentation value
 */
function getReturnsDoc(program, target) {
    return getDocDataInternal(program, target, "returns")?.value;
}
const $errorsDoc = (context, target, text) => {
    validateDecoratorUniqueOnNode(context, target, $doc);
    setDocData(context.program, target, "errors", { value: text, source: "decorator" });
};
/**
 * Get the documentation information for the return errors types of an operation. In most cases you probably just want to use {@link getErrorsDoc}
 * @param program Program
 * @param target Type
 * @returns Doc data with source information.
 */
function getErrorsDocData(program, target) {
    return getDocDataInternal(program, target, "errors");
}
/**
 * Get the documentation string for the return errors types of an operation.
 * @param program Program
 * @param target Type
 * @returns Documentation value
 */
function getErrorsDoc(program, target) {
    return getDocDataInternal(program, target, "errors")?.value;
}
const $inspectType = (context, target, text) => {
    // eslint-disable-next-line no-console
    if (text)
        console.log(text);
    // eslint-disable-next-line no-console
    console.dir(target, { depth: 3 });
};
const $inspectTypeName = (context, target, text) => {
    // eslint-disable-next-line no-console
    if (text)
        console.log(text);
    // eslint-disable-next-line no-console
    console.log(getTypeName(target));
};
function isStringType(program, target) {
    const coreType = program.checker.getStdType("string");
    const stringType = target.projector ? target.projector.projectType(coreType) : coreType;
    return (target.kind === "Scalar" && program.checker.isTypeAssignableTo(target, stringType, target)[0]);
}
function isNumericType(program, target) {
    const coreType = program.checker.getStdType("numeric");
    const numericType = target.projector ? target.projector.projectType(coreType) : coreType;
    return (target.kind === "Scalar" && program.checker.isTypeAssignableTo(target, numericType, target)[0]);
}
/**
 * Check the given type is matching the given condition or is a union of null and types matching the condition.
 * @param type Type to test
 * @param condition Condition
 * @returns Boolean
 */
function isTypeIn(type, condition) {
    if (type.kind === "Union") {
        return [...type.variants.values()].some((v) => condition(v.type));
    }
    return condition(type);
}
function validateTargetingANumeric(context, target, decoratorName) {
    const valid = isTypeIn(getPropertyType(target), (x) => isNumericType(context.program, x));
    if (!valid) {
        reportDiagnostic(context.program, {
            code: "decorator-wrong-target",
            format: {
                decorator: decoratorName,
                to: `type it is not a numeric`,
            },
            target: context.decoratorTarget,
        });
    }
    return valid;
}
/**
 * Validate the given target is a string type or a union containing at least a string type.
 */
function validateTargetingAString(context, target, decoratorName) {
    const valid = isTypeIn(getPropertyType(target), (x) => isStringType(context.program, x));
    if (!valid) {
        reportDiagnostic(context.program, {
            code: "decorator-wrong-target",
            format: {
                decorator: decoratorName,
                to: `type it is not a string`,
            },
            target: context.decoratorTarget,
        });
    }
    return valid;
}
// -- @error decorator ----------------------
const [getErrorState, setErrorState] = useStateSet("error");
/**
 * `@error` decorator marks a model as an error type.
 *  Any derived models (using extends) will also be seen as error types.
 */
const $error = (context, entity) => {
    validateDecoratorUniqueOnNode(context, entity, $error);
    setErrorState(context.program, entity);
};
/**
 * Check if the type is an error model or a descendant of an error model.
 */
function isErrorModel(program, target) {
    if (target.kind !== "Model") {
        return false;
    }
    let current = target;
    while (current) {
        if (getErrorState(program, current)) {
            return true;
        }
        current = current.baseModel;
    }
    return false;
}
// -- @format decorator ---------------------
const [getFormat, setFormat] = useStateMap("format");
/**
 * `@format` - specify the data format hint for a string type
 *
 * The first argument is a string that identifies the format that the string type expects.  Any string
 * can be entered here, but a TypeSpec emitter must know how to interpret
 *
 * For TypeSpec specs that will be used with an OpenAPI emitter, the OpenAPI specification describes possible
 * valid values for a string type's format:
 *
 * https://github.com/OAI/OpenAPI-Specification/blob/3.0.3/versions/3.0.3.md#dataTypes
 *
 * `@format` can be specified on a type that extends from `string` or a `string`-typed model property.
 */
const $format = (context, target, format) => {
    validateDecoratorUniqueOnNode(context, target, $format);
    if (!validateTargetingAString(context, target, "@format")) {
        return;
    }
    const targetType = getPropertyType(target);
    if (targetType.kind === "Scalar" && isIntrinsicType(context.program, targetType, "bytes")) {
        reportDeprecated(context.program, "Using `@format` on a bytes scalar is deprecated. Use `@encode` instead. https://github.com/microsoft/typespec/issues/1873", target);
    }
    setFormat(context.program, target, format);
};
// -- @pattern decorator ---------------------
const [getPatternData, setPatternData] = useStateMap("patternValues");
const $pattern = (context, target, pattern, validationMessage) => {
    validateDecoratorUniqueOnNode(context, target, $pattern);
    if (!validateTargetingAString(context, target, "@pattern")) {
        return;
    }
    const patternData = {
        pattern,
        validationMessage,
    };
    setPatternData(context.program, target, patternData);
};
/**
 * Gets the pattern regular expression associated with a given type, if one has been set.
 *
 * @see getPatternData
 *
 * @param program - the Program containing the target Type
 * @param target - the type to get the pattern for
 * @returns the pattern string, if one was set
 */
function getPattern(program, target) {
    return getPatternData(program, target)?.pattern;
}
// -- @minLength decorator ---------------------
const $minLength = (context, target, minLength) => {
    validateDecoratorUniqueOnNode(context, target, $minLength);
    if (!validateTargetingAString(context, target, "@minLength") ||
        !validateRange(context, minLength, getMaxLengthAsNumeric(context.program, target))) {
        return;
    }
    setMinLength(context.program, target, minLength);
};
// -- @maxLength decorator ---------------------
const $maxLength = (context, target, maxLength) => {
    validateDecoratorUniqueOnNode(context, target, $maxLength);
    if (!validateTargetingAString(context, target, "@maxLength") ||
        !validateRange(context, getMinLengthAsNumeric(context.program, target), maxLength)) {
        return;
    }
    setMaxLength(context.program, target, maxLength);
};
// -- @minItems decorator ---------------------
const $minItems = (context, target, minItems) => {
    validateDecoratorUniqueOnNode(context, target, $minItems);
    if (!isArrayModelType(context.program, target.kind === "Model" ? target : target.type)) {
        reportDiagnostic(context.program, {
            code: "decorator-wrong-target",
            format: {
                decorator: "@minItems",
                to: `non Array type`,
            },
            target: context.decoratorTarget,
        });
    }
    if (!validateRange(context, minItems, getMaxItemsAsNumeric(context.program, target))) {
        return;
    }
    setMinItems(context.program, target, minItems);
};
// -- @maxLength decorator ---------------------
const $maxItems = (context, target, maxItems) => {
    validateDecoratorUniqueOnNode(context, target, $maxItems);
    if (!isArrayModelType(context.program, target.kind === "Model" ? target : target.type)) {
        reportDiagnostic(context.program, {
            code: "decorator-wrong-target",
            format: {
                decorator: "@maxItems",
                to: `non Array type`,
            },
            target: context.decoratorTarget,
        });
    }
    if (!validateRange(context, getMinItemsAsNumeric(context.program, target), maxItems)) {
        return;
    }
    setMaxItems(context.program, target, maxItems);
};
// -- @minValue decorator ---------------------
const $minValue = (context, target, minValue) => {
    validateDecoratorUniqueOnNode(context, target, $minValue);
    validateDecoratorNotOnType(context, target, $minValueExclusive, $minValue);
    const { program } = context;
    if (!validateTargetingANumeric(context, target, "@minValue")) {
        return;
    }
    if (!validateRange(context, minValue, getMaxValueAsNumeric(context.program, target) ??
        getMaxValueExclusiveAsNumeric(context.program, target))) {
        return;
    }
    setMinValue(program, target, minValue);
};
// -- @maxValue decorator ---------------------
const $maxValue = (context, target, maxValue) => {
    validateDecoratorUniqueOnNode(context, target, $maxValue);
    validateDecoratorNotOnType(context, target, $maxValueExclusive, $maxValue);
    const { program } = context;
    if (!validateTargetingANumeric(context, target, "@maxValue")) {
        return;
    }
    if (!validateRange(context, getMinValueAsNumeric(context.program, target) ??
        getMinValueExclusiveAsNumeric(context.program, target), maxValue)) {
        return;
    }
    setMaxValue(program, target, maxValue);
};
// -- @minValueExclusive decorator ---------------------
const $minValueExclusive = (context, target, minValueExclusive) => {
    validateDecoratorUniqueOnNode(context, target, $minValueExclusive);
    validateDecoratorNotOnType(context, target, $minValue, $minValueExclusive);
    const { program } = context;
    if (!validateTargetingANumeric(context, target, "@minValueExclusive")) {
        return;
    }
    if (!validateRange(context, minValueExclusive, getMaxValueAsNumeric(context.program, target) ??
        getMaxValueExclusiveAsNumeric(context.program, target))) {
        return;
    }
    setMinValueExclusive(program, target, minValueExclusive);
};
// -- @maxValueExclusive decorator ---------------------
const $maxValueExclusive = (context, target, maxValueExclusive) => {
    validateDecoratorUniqueOnNode(context, target, $maxValueExclusive);
    validateDecoratorNotOnType(context, target, $maxValue, $maxValueExclusive);
    const { program } = context;
    if (!validateTargetingANumeric(context, target, "@maxValueExclusive")) {
        return;
    }
    if (!validateRange(context, getMinValueAsNumeric(context.program, target) ??
        getMinValueExclusiveAsNumeric(context.program, target), maxValueExclusive)) {
        return;
    }
    setMaxValueExclusive(program, target, maxValueExclusive);
};
// -- @secret decorator ---------------------
const [isSecret, markSecret] = useStateSet("secretTypes");
/**
 * Mark a string as a secret value that should be treated carefully to avoid exposure
 * @param context Decorator context
 * @param target Decorator target, either a string model or a property with type string.
 */
const $secret = (context, target) => {
    validateDecoratorUniqueOnNode(context, target, $secret);
    if (!validateTargetingAString(context, target, "@secret")) {
        return;
    }
    markSecret(context.program, target);
};
const [getEncode, setEncodeData] = useStateMap("encode");
const $encode = (context, target, encoding, encodeAs) => {
    validateDecoratorUniqueOnNode(context, target, $encode);
    const encodeData = computeEncoding(context.program, encoding, encodeAs);
    if (encodeData === undefined) {
        return;
    }
    const targetType = getPropertyType(target);
    validateEncodeData(context, targetType, encodeData);
    setEncodeData(context.program, target, encodeData);
};
function computeEncoding(program, encodingOrEncodeAs, encodeAs) {
    const strType = program.checker.getStdType("string");
    const resolvedEncodeAs = encodeAs ?? strType;
    if (typeof encodingOrEncodeAs === "string") {
        return { encoding: encodingOrEncodeAs, type: resolvedEncodeAs };
    }
    else if (isValue(encodingOrEncodeAs)) {
        const member = encodingOrEncodeAs.value;
        if (member.value && typeof member.value === "string") {
            return { encoding: member.value, type: resolvedEncodeAs };
        }
        else {
            return { encoding: getTypeName(member), type: resolvedEncodeAs };
        }
    }
    else {
        const originalType = encodingOrEncodeAs.projectionBase ?? encodingOrEncodeAs;
        if (originalType !== strType) {
            reportDiagnostic(program, {
                code: "invalid-encode",
                messageId: "firstArg",
                target: encodingOrEncodeAs,
            });
            return undefined;
        }
        return { type: encodingOrEncodeAs };
    }
}
function validateEncodeData(context, target, encodeData) {
    function check(validTargets, validEncodeTypes) {
        const checker = context.program.checker;
        const isTargetValid = isTypeIn(target.projectionBase ?? target, (type) => validTargets.some((validTarget) => {
            return ignoreDiagnostics(checker.isTypeAssignableTo(type, checker.getStdType(validTarget), target));
        }));
        if (!isTargetValid) {
            reportDiagnostic(context.program, {
                code: "invalid-encode",
                messageId: "wrongType",
                format: {
                    encoding: encodeData.encoding ?? "string",
                    type: getTypeName(target),
                    expected: validTargets.join(", "),
                },
                target: context.decoratorTarget,
            });
        }
        const isEncodingTypeValid = validEncodeTypes.some((validEncoding) => {
            return ignoreDiagnostics(checker.isTypeAssignableTo(encodeData.type.projectionBase ?? encodeData.type, checker.getStdType(validEncoding), target));
        });
        if (!isEncodingTypeValid) {
            const typeName = getTypeName(encodeData.type.projectionBase ?? encodeData.type);
            reportDiagnostic(context.program, {
                code: "invalid-encode",
                messageId: ["unixTimestamp", "seconds"].includes(encodeData.encoding ?? "string")
                    ? "wrongNumericEncodingType"
                    : "wrongEncodingType",
                format: {
                    encoding: encodeData.encoding,
                    type: getTypeName(target),
                    expected: validEncodeTypes.join(", "),
                    actual: typeName,
                },
                target: context.decoratorTarget,
            });
        }
    }
    switch (encodeData.encoding) {
        case "rfc3339":
            return check(["utcDateTime", "offsetDateTime"], ["string"]);
        case "rfc7231":
            return check(["utcDateTime", "offsetDateTime"], ["string"]);
        case "unixTimestamp":
            return check(["utcDateTime"], ["integer"]);
        case "seconds":
            return check(["duration"], ["numeric"]);
        case "base64":
            return check(["bytes"], ["string"]);
        case "base64url":
            return check(["bytes"], ["string"]);
        case undefined:
            return check(["numeric"], ["string"]);
    }
}
// -- @visibility decorator ---------------------
const [getVisibility, setVisibility, getVisibilityStateMap] = useStateMap("visibilitySettings");
const $visibility = (context, target, ...visibilities) => {
    validateDecoratorUniqueOnNode(context, target, $visibility);
    setVisibility(context.program, target, visibilities);
};
function clearVisibilities(program, target) {
    getVisibilityStateMap(program).delete(target);
}
const $withVisibility = (context, target, ...visibilities) => {
    filterModelPropertiesInPlace(target, (p) => isVisible(context.program, p, visibilities));
    [...target.properties.values()].forEach((p) => clearVisibilities(context.program, p));
};
function isVisible(program, property, visibilities) {
    const propertyVisibilities = getVisibility(program, property);
    return !propertyVisibilities || propertyVisibilities.some((v) => visibilities.includes(v));
}
function filterModelPropertiesInPlace(model, filter) {
    for (const [key, prop] of model.properties) {
        if (!filter(prop)) {
            model.properties.delete(key);
        }
    }
}
// -- @withOptionalProperties decorator ---------------------
const $withOptionalProperties = (context, target) => {
    // Make all properties of the target type optional
    target.properties.forEach((p) => (p.optional = true));
};
// -- @withUpdateableProperties decorator ----------------------
const $withUpdateableProperties = (context, target) => {
    if (!validateDecoratorTarget(context, target, "@withUpdateableProperties", "Model")) {
        return;
    }
    filterModelPropertiesInPlace(target, (p) => isVisible(context.program, p, ["update"]));
};
// -- @withoutOmittedProperties decorator ----------------------
const $withoutOmittedProperties = (context, target, omitProperties) => {
    // Get the property or properties to omit
    const omitNames = new Set();
    if (omitProperties.kind === "String") {
        omitNames.add(omitProperties.value);
    }
    else if (omitProperties.kind === "Union") {
        for (const variant of omitProperties.variants.values()) {
            if (variant.type.kind === "String") {
                omitNames.add(variant.type.value);
            }
        }
    }
    // Remove all properties to be omitted
    filterModelPropertiesInPlace(target, (prop) => !omitNames.has(prop.name));
};
// -- @withPickedProperties decorator ----------------------
const $withPickedProperties = (context, target, pickedProperties) => {
    // Get the property or properties to pick
    const pickedNames = new Set();
    if (pickedProperties.kind === "String") {
        pickedNames.add(pickedProperties.value);
    }
    else if (pickedProperties.kind === "Union") {
        for (const variant of pickedProperties.variants.values()) {
            if (variant.type.kind === "String") {
                pickedNames.add(variant.type.value);
            }
        }
    }
    // Remove all properties not picked
    filterModelPropertiesInPlace(target, (prop) => pickedNames.has(prop.name));
};
// -- @withoutDefaultValues decorator ----------------------
const $withoutDefaultValues = (context, target) => {
    // remove all read-only properties from the target type
    target.properties.forEach((p) => {
        // eslint-disable-next-line @typescript-eslint/no-deprecated
        delete p.default;
        delete p.defaultValue;
    });
};
// -- @tag decorator ---------------------
const [getTagsState, setTags] = useStateMap("tagProperties");
// Set a tag on an operation, interface, or namespace.  There can be multiple tags on an
// operation, interface, or namespace.
const $tag = (context, target, tag) => {
    const tags = getTagsState(context.program, target);
    if (tags) {
        tags.push(tag);
    }
    else {
        setTags(context.program, target, [tag]);
    }
};
// Return the tags set on an operation or namespace
function getTags(program, target) {
    return getTagsState(program, target) || [];
}
// Merge the tags for a operation with the tags that are on the namespace or
// interface it resides within.
function getAllTags(program, target) {
    const tags = new Set();
    let current = target;
    while (current !== undefined) {
        for (const t of getTags(program, current)) {
            tags.add(t);
        }
        // Move up to the parent
        if (current.kind === "Operation") {
            current = current.interface ?? current.namespace;
        }
        else {
            // Type is a namespace or interface
            current = current.namespace;
        }
    }
    return tags.size > 0 ? Array.from(tags).reverse() : undefined;
}
// -- @friendlyName decorator ---------------------
const [getFriendlyName, setFriendlyName] = useStateMap("friendlyNames");
const $friendlyName = (context, target, friendlyName, sourceObject) => {
    // workaround for current lack of functionality in compiler
    // https://github.com/microsoft/typespec/issues/2717
    if (target.kind === "Model" || target.kind === "Operation") {
        if (context.decoratorTarget.kind === SyntaxKind.AugmentDecoratorStatement) {
            if (ignoreDiagnostics(context.program.checker.resolveTypeReference(context.decoratorTarget.targetType))?.node !== target.node) {
                return;
            }
        }
        if (context.decoratorTarget.kind === SyntaxKind.DecoratorExpression) {
            if (context.decoratorTarget.parent !== target.node) {
                return;
            }
        }
    }
    // If an object was passed in, use it to format the friendly name
    if (sourceObject) {
        friendlyName = replaceTemplatedStringFromProperties(friendlyName, sourceObject);
    }
    setFriendlyName(context.program, target, friendlyName);
};
const [getKnownValues, setKnownValues] = useStateMap("knownValues");
/**
 * `@knownValues` marks a string type with an enum that contains all known values
 *
 * The first parameter is a reference to an enum type that describes all possible values that the
 * type accepts.
 *
 * `@knownValues` can only be applied to model types that extend `string`.
 *
 * @param target Decorator target. Must be a string. (model Foo extends string)
 * @param knownValues Must be an enum.
 */
const $knownValues = (context, target, knownValues) => {
    const type = getPropertyType(target);
    if (!isStringType(context.program, type) && !isNumericType(context.program, type)) {
        context.program.reportDiagnostic(createDiagnostic({
            code: "decorator-wrong-target",
            format: { decorator: "@knownValues", to: "type, it is  not a string or numeric" },
            target,
        }));
        return;
    }
    for (const member of knownValues.members.values()) {
        const propertyType = getPropertyType(target);
        if (!isEnumMemberAssignableToType(context.program, propertyType, member)) {
            reportDiagnostic(context.program, {
                code: "known-values-invalid-enum",
                format: {
                    member: member.name,
                    type: getTypeName(propertyType),
                },
                target,
            });
            return;
        }
    }
    setKnownValues(context.program, target, knownValues);
};
function isEnumMemberAssignableToType(program, typeName, member) {
    const memberType = member.value !== undefined ? typeof member.value : "string";
    switch (memberType) {
        case "string":
            return isStringType(program, typeName);
        case "number":
            return isNumericType(program, typeName);
        default:
            return false;
    }
}
const [getKey, setKey] = useStateMap("key");
/**
 * `@key` - mark a model property as the key to identify instances of that type
 *
 * The optional first argument accepts an alternate key name which may be used by emitters.
 * Otherwise, the name of the target property will be used.
 *
 * `@key` can only be applied to model properties.
 */
const $key = (context, entity, altName) => {
    // Ensure that the key property is not marked as optional
    if (entity.optional) {
        reportDiagnostic(context.program, {
            code: "no-optional-key",
            format: { propertyName: entity.name },
            target: entity,
        });
        return;
    }
    // Register the key property
    setKey(context.program, entity, altName || entity.name);
};
function isKey(program, property) {
    return getKey(program, property) !== undefined;
}
function getKeyName(program, property) {
    return getKey(program, property);
}
const $withDefaultKeyVisibility = (context, entity, visibility) => {
    const keyProperties = [];
    entity.properties.forEach((prop) => {
        // Keep track of any key property without a visibility
        if (isKey(context.program, prop) && !getVisibility(context.program, prop)) {
            keyProperties.push(prop);
        }
    });
    // For each key property without a visibility, clone it and add the specified
    // default visibility value
    keyProperties.forEach((keyProp) => {
        entity.properties.set(keyProp.name, context.program.checker.cloneType(keyProp, {
            decorators: [
                ...keyProp.decorators,
                {
                    decorator: $visibility,
                    args: [
                        { value: context.program.checker.createLiteralType(visibility), jsValue: visibility },
                    ],
                },
            ],
        }));
    });
};
/**
 * Mark a type as deprecated
 * @param context DecoratorContext
 * @param target Decorator target
 * @param message Deprecation target.
 *
 * @example
 * ``` @deprecated("Foo is deprecated, use Bar instead.")
 *     model Foo {}
 * ```
 */
// eslint-disable-next-line @typescript-eslint/no-deprecated
const $deprecated = (context, target, message) => {
    markDeprecated(context.program, target, { message });
};
/**
 * Return the deprecated message or undefined if not deprecated
 * @param program Program
 * @param type Type
 */
function getDeprecated(program, type) {
    return getDeprecationDetails(program, type)?.message;
}
const [getOverloads, setOverloads] = useStateMap("overloadedByKey");
const [getOverloadedOperation, setOverloadBase] = useStateMap("overloadsOperation");
/**
 * `@overload` - Indicate that the target overloads (specializes) the overloads type.
 * @param context DecoratorContext
 * @param target The specializing operation declaration
 * @param overloadBase The operation to be overloaded.
 */
const $overload = (context, target, overloadBase) => {
    // Ensure that the overloaded method arguments are a subtype of the original operation.
    const [paramValid, paramDiagnostics] = context.program.checker.isTypeAssignableTo(target.parameters.projectionBase ?? target.parameters, overloadBase.parameters.projectionBase ?? overloadBase.parameters, target);
    if (!paramValid)
        context.program.reportDiagnostics(paramDiagnostics);
    const [returnTypeValid, returnTypeDiagnostics] = context.program.checker.isTypeAssignableTo(target.returnType.projectionBase ?? target.returnType, overloadBase.returnType.projectionBase ?? overloadBase.returnType, target);
    if (!returnTypeValid)
        context.program.reportDiagnostics(returnTypeDiagnostics);
    if (!areOperationsInSameContainer(target, overloadBase)) {
        reportDiagnostic(context.program, {
            code: "overload-same-parent",
            target: context.decoratorTarget,
        });
    }
    // Save the information about the overloaded operation
    setOverloadBase(context.program, target, overloadBase);
    const existingOverloads = getOverloads(context.program, overloadBase) || new Array();
    setOverloads(context.program, overloadBase, existingOverloads.concat(target));
};
function areOperationsInSameContainer(op1, op2) {
    return op1.interface || op2.interface
        ? equalsWithoutProjection(op1.interface, op2.interface)
        : op1.namespace === op2.namespace;
}
// note: because the 'interface' property of Operation types is projected after the
// type is finalized, the target operation or overloadBase may reference an un-projected
// interface at the time of decorator execution during projections.  This normalizes
// the interfaces to their unprojected form before comparison.
function equalsWithoutProjection(interface1, interface2) {
    if (interface1 === undefined || interface2 === undefined)
        return false;
    return getBaseInterface(interface1) === getBaseInterface(interface2);
}
function getBaseInterface(int1) {
    return int1.projectionSource === undefined
        ? int1
        : getBaseInterface(int1.projectionSource);
}
const projectedNameKey = createStateSymbol("projectedNameKey");
/**
 * `@projectedName` - Indicate that this entity should be renamed according to the given projection.
 * @param context DecoratorContext
 * @param target The that should have a different name.
 * @param projectionName Name of the projection (e.g. "toJson", "toCSharp")
 * @param projectedName Name of the type should have in the scope of the projection specified.
 */
const $projectedName = (context, target, projectionName, projectedName) => {
    let map = context.program.stateMap(projectedNameKey).get(target);
    if (map === undefined) {
        map = new Map();
        context.program.stateMap(projectedNameKey).set(target, map);
    }
    map.set(projectionName, projectedName);
};
/**
 * @param program Program
 * @param target Target
 * @returns Map of the projected names for the given entity.
 */
function getProjectedNames(program, target) {
    return program.stateMap(projectedNameKey).get(target);
}
/**
 * Get the projected name of the given entity for the given projection.
 * @param program Program
 * @param target Target
 * @returns Projected name for the given projection
 */
function getProjectedName(program, target, projectionName) {
    return getProjectedNames(program, target)?.get(projectionName);
}
/**
 * Get the projected name of the given entity for the given projection.
 * @param program Program
 * @param target Target
 * @returns Projected name for the given projection
 */
function hasProjectedName(program, target, projectionName) {
    return getProjectedNames(program, target)?.has(projectionName) ?? false;
}
function validateRange(context, min, max) {
    if (min === undefined || max === undefined) {
        return true;
    }
    if (min.gt(max)) {
        reportDiagnostic(context.program, {
            code: "invalid-range",
            format: { start: min.toString(), end: max.toString() },
            target: context.decoratorTarget,
        });
        return false;
    }
    return true;
}
const $discriminator = (context, entity, propertyName) => {
    const discriminator = { propertyName };
    if (entity.kind === "Union") {
        // we can validate discriminator up front for unions. Models are validated in the accessor as we might not have the reference to all derived types at this time.
        const [, diagnostics] = getDiscriminatedUnion(entity, discriminator);
        if (diagnostics.length > 0) {
            context.program.reportDiagnostics(diagnostics);
            return;
        }
    }
    setDiscriminator(context.program, entity, discriminator);
};
const [getParameterVisibility, setParameterVisibility] = useStateMap("parameterVisibility");
const $parameterVisibility = (context, entity, ...visibilities) => {
    validateDecoratorUniqueOnNode(context, entity, $parameterVisibility);
    setParameterVisibility(context.program, entity, visibilities);
};
const [getReturnTypeVisibility, setReturnTypeVisibility] = useStateMap("returnTypeVisibility");
const $returnTypeVisibility = (context, entity, ...visibilities) => {
    validateDecoratorUniqueOnNode(context, entity, $returnTypeVisibility);
    setReturnTypeVisibility(context.program, entity, visibilities);
};
const [getExamplesState, setExamples] = useStateMap("examples");
const $example = (context, target, _example, options) => {
    const decorator = target.decorators.find((d) => d.decorator === $example && d.node === context.decoratorTarget);
    compilerAssert(decorator, `Couldn't find @example decorator`, context.decoratorTarget);
    const rawExample = decorator.args[0].value;
    // skip validation in projections
    if (target.projectionBase === undefined) {
        if (!checkExampleValid(context.program, rawExample, target.kind === "ModelProperty" ? target.type : target, context.getArgumentTarget(0))) {
            return;
        }
    }
    let list = getExamplesState(context.program, target);
    if (list === undefined) {
        list = [];
        setExamples(context.program, target, list);
    }
    list.push({ value: rawExample, ...options });
};
function getExamples(program, target) {
    return getExamplesState(program, target) ?? [];
}
const [getOpExamplesState, setOpExamples] = useStateMap("opExamples");
const $opExample = (context, target, _example, options) => {
    const decorator = target.decorators.find((d) => d.decorator === $opExample && d.node === context.decoratorTarget);
    compilerAssert(decorator, `Couldn't find @opExample decorator`, context.decoratorTarget);
    const rawExampleConfig = decorator.args[0].value;
    const parameters = rawExampleConfig.properties.get("parameters")?.value;
    const returnType = rawExampleConfig.properties.get("returnType")?.value;
    // skip validation in projections
    if (target.projectionBase === undefined) {
        if (parameters &&
            !checkExampleValid(context.program, parameters, target.parameters, context.getArgumentTarget(0))) {
            return;
        }
        if (returnType &&
            !checkExampleValid(context.program, returnType, target.returnType, context.getArgumentTarget(0))) {
            return;
        }
    }
    let list = getOpExamplesState(context.program, target);
    if (list === undefined) {
        list = [];
        setOpExamples(context.program, target, list);
    }
    list.push({ parameters, returnType, ...options });
};
function checkExampleValid(program, value, target, diagnosticTarget) {
    const exactType = program.checker.getValueExactType(value);
    const [assignable, diagnostics] = program.checker.isTypeAssignableTo(exactType ?? value.type, target, diagnosticTarget);
    if (!assignable) {
        program.reportDiagnostics(diagnostics);
    }
    return assignable;
}
function getOpExamples(program, target) {
    return getOpExamplesState(program, target) ?? [];
}

export { $encode as $, $maxLength as A, $minItems as B, $maxItems as C, $minValue as D, $maxValue as E, $minValueExclusive as F, $maxValueExclusive as G, $secret as H, $tag as I, $friendlyName as J, $knownValues as K, $key as L, $overload as M, $projectedName as N, $discriminator as O, $example as P, $opExample as Q, $visibility as R, $withVisibility as S, $inspectType as T, $inspectTypeName as U, $parameterVisibility as V, $returnTypeVisibility as W, getProjectedName as X, hasProjectedName as Y, cadlTypeToJson as Z, createDecoratorDefinition as _, getFormat as a, getAllTags as a0, getDeprecated as a1, getDoc as a2, getErrorsDoc as a3, getErrorsDocData as a4, getExamples as a5, getFriendlyName as a6, getKeyName as a7, getKnownValues as a8, getOpExamples as a9, getOverloadedOperation as aa, getOverloads as ab, getParameterVisibility as ac, getPattern as ad, getPatternData as ae, getProjectedNames as af, getPropertyType as ag, getReturnTypeVisibility as ah, getReturnsDoc as ai, getReturnsDocData as aj, getSummary as ak, getTags as al, isCadlValueTypeOf as am, isErrorModel as an, isKey as ao, isSecret as ap, isTypeSpecValueTypeOf as aq, isVisible as ar, namespace as as, typespecTypeToJson as at, validateDecoratorNotOnType as au, validateDecoratorParamCount as av, validateDecoratorParamType as aw, validateDecoratorTarget as ax, validateDecoratorTargetIntrinsic as ay, getVisibility as b, unsafe_useStateSet as c, useStateMap as d, useStateSet as e, isStringType as f, getEncode as g, isNumericType as h, isIntrinsicType as i, $doc as j, $withOptionalProperties as k, $withUpdateableProperties as l, $withoutOmittedProperties as m, $withPickedProperties as n, $withoutDefaultValues as o, $withDefaultKeyVisibility as p, $summary as q, $returnsDoc as r, $errorsDoc as s, $deprecated as t, unsafe_useStateMap as u, validateDecoratorUniqueOnNode as v, $error as w, $format as x, $pattern as y, $minLength as z };
