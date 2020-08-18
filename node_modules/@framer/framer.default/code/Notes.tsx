import * as React from "react"
import { Stack, useCycle, addPropertyControls, ControlType, RenderTarget } from "framer"
import { indentTitle } from "./lib/indentTitle"
import { defaultEvents } from "./lib/constants"

/*
 **   STICKY
 **
 ** - type should scale for tiny ones
 ** - fix truncation
 ** - "approved/done" yes, no - makes a checkmark appear on it
 */

const colors = {
    blue: "#77DDFF",
    yellow: "#FFEE66",
    white: "#FFFFFF",
    pink: "#FF77AA",
    green: "#55DD88",
    red: "#FF4477",
}

export function Notes(props) {
    const {
        note = "",
        color,
        preview,
        alignment,
        smallFont,
        onClick,
        onMouseEnter,
        onMouseLeave,
        onMouseDown,
        onMouseUp,
    } = props

    return (
        <Stack
            size={"100%"}
            center
            background={colors[color]}
            distribution={"center"}
            style={{
                visibility: RenderTarget.current() === RenderTarget.preview && !preview ? "hidden" : "visible",
                fontFamily: "Nanum Pen Script",
                //@ts-ignore
                fontDisplay: "fallback",
            }}
            gap={0}
            shadow="  0 0.5px 1.4px rgba(0, 0, 0, 0.024),
            0 1.3px 3.8px rgba(0, 0, 0, 0.035),
            0 3px 9px rgba(0, 0, 0, 0.046),
            0 10px 30px rgba(0, 0, 0, 0.07)"
            borderRadius={8}
            {...{ onClick, onMouseEnter, onMouseLeave, onMouseDown, onMouseUp }}
        >
            <link href="https://fonts.googleapis.com/css?family=Nanum+Pen+Script&display=swap" rel="stylesheet" />
            <Stack
                style={{ flex: 1, width: "100%" }}
                paddingTop={12}
                paddingBottom={0}
                paddingLeft={smallFont ? 15 : 18}
                paddingRight={smallFont ? 15 : 18}
                overflow="hidden"
            >
                <p
                    style={{
                        width: "100%",
                        fontSize: smallFont ? 18 : 32,
                        overflowWrap: "break-word",
                        lineHeight: smallFont ? 1.15 : 1.08,
                        textAlign: alignment,
                        color: note.length > 0 ? "rgba(0,0,0,0.7)" : "rgba(0,0,0,0.25)",

                        display: "-webkit-box",
                        overflow: "hidden",
                        // lineClamp: 7,
                        WebkitBoxOrient: "vertical",
                        // WebkitLineClamp: 7,
                        whiteSpace: "pre-wrap",
                    }}
                >
                    {note.length > 0 ? note : "Write something..."}
                </p>
            </Stack>
        </Stack>
    )
}

addPropertyControls(Notes, {
    note: {
        type: ControlType.String,
        displayTextArea: true,
        placeholder: `Write something… \n\n\n`,
    },
    color: {
        type: ControlType.Enum,
        defaultValue: "yellow",
        options: Object.keys(colors),
        optionTitles: Object.keys(colors).map((c) => c.replace(/^\w/, (c) => c.toUpperCase())),
    },

    alignment: {
        title: "Text Align",
        type: ControlType.SegmentedEnum,
        optionTitles: ["Left", "Center", "Right"],
        options: ["left", "center", "right"],
    },
    smallFont: {
        type: ControlType.Boolean,
        disabledTitle: "Big",
        enabledTitle: "Small",
        title: "Text Size",
    },
    preview: {
        type: ControlType.Boolean,
        defaultValue: true,
        title: "In Preview",
        enabledTitle: "Show",
        disabledTitle: "Hide",
    },
    ...defaultEvents,
})

Notes.displayName = "Sticky Note"
