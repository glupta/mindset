import { PropertyControls, ControlType } from "framer"
import { indentTitle } from "./indentTitle"

export const fontStack = `"Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"`

export const emptyStateStyle: React.CSSProperties = {
    width: "100%",
    height: "100%",
    borderRadius: 6,
    background: "rgba(136, 85, 255, 0.3)",
    border: "1px dashed #85F",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
}

export const defaultEvents: PropertyControls = {
    onClick: {
        type: ControlType.EventHandler,
    },
    // onMouseDown: {
    //     type: ControlType.EventHandler,
    // },
    // onMouseUp: {
    //     type: ControlType.EventHandler,
    // },
    onMouseEnter: {
        type: ControlType.EventHandler,
    },
    onMouseLeave: {
        type: ControlType.EventHandler,
    },
}

export const fontControls: PropertyControls = {
    font: {
        type: ControlType.Boolean,
        title: "Font",
        defaultValue: false,
        disabledTitle: "Default",
        enabledTitle: "Custom",
    },
    fontFamily: {
        type: ControlType.String,
        title: indentTitle("Family"),
        placeholder: "Inter",
        hidden: ({ font }) => !font,
    },
    fontWeight: {
        type: ControlType.Enum,
        title: indentTitle("Weight"),
        options: [100, 200, 300, 400, 500, 600, 700, 800, 900],
        optionTitles: ["Thin", "Extra-light", "Light", "Regular", "Medium", "Semi-bold", "Bold", "Extra-bold", "Black"],
        hidden: ({ font }) => !font,
    },
}
