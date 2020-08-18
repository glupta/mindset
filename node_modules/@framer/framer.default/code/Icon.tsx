import * as React from "react"
import { addPropertyControls, ControlType, Color, motion } from "framer"
import * as FeatherIcons from "react-feather"
import { indentTitle } from "./lib/indentTitle"
import { emptyStateStyle, defaultEvents } from "./lib/constants"

/*
 ** ICON
 ** - Add other icon libraries if it doesn't impact bundle size too much
 ** - make this a custom component with full icons and such
 */

export interface IconProps {
    width: number
    height: number
    color?: Color
    selection?: boolean
    iconSearch?: string
    iconSelection?: string
    onTap?: any
    onClick?: any
    onMouseEnter?: any
    onMouseLeave?: any
    onMouseDown?: any
    onMouseUp?: any
}

export function Icon(props: IconProps) {
    const {
        width,
        height,
        color,
        selection,
        iconSearch,
        iconSelection,
        onClick,
        onMouseDown,
        onMouseUp,
        onMouseEnter,
        onMouseLeave,
    } = props
    const iconSearchTerm = iconSearch ? iconSearch : "Framer"
    const name = selection
        ? iconSelection
        : iconSearchTerm
              .toLowerCase()
              .split("-")
              .map((piece) => piece.charAt(0).toUpperCase() + piece.slice(1))
              .join("")

    const TagName = FeatherIcons[name]

    return (
        <motion.div style={{ display: "contents" }} {...{ onClick, onMouseEnter, onMouseLeave }}>
            {TagName ? (
                <TagName icon={name} width={width} height={height} color={color} />
            ) : (
                <NullState
                    {...{
                        onClick,
                        onMouseDown,
                        onMouseUp,
                        onMouseEnter,
                        onMouseLeave,
                    }}
                />
            )}
        </motion.div>
    )
}

function NullState({ onClick, onMouseDown, onMouseUp, onMouseEnter, onMouseLeave }) {
    return (
        <div {...{ onClick, onMouseDown, onMouseUp, onMouseEnter, onMouseLeave }} style={emptyStateStyle}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" style={iconStyle}>
                <path
                    d="M 12.857 0 C 19.958 0 25.714 5.756 25.714 12.857 C 25.714 19.958 19.958 25.714 12.857 25.714 C 5.756 25.714 0 19.958 0 12.857 C 0 5.756 5.756 0 12.857 0 Z"
                    fill="#FFFFFF"
                ></path>
                <path
                    d="M 20.357 20.357 L 27.857 27.857"
                    fill="transparent"
                    stroke-width="4.28"
                    stroke="#FFFFFF"
                    stroke-linecap="round"
                ></path>
                <g transform="translate(9.643 6.429)">
                    <path
                        d="M 3.214 12.857 L 3.214 12.857"
                        fill="transparent"
                        stroke-width="3.75"
                        stroke="#8A58FF"
                        stroke-linecap="round"
                    ></path>
                    <path
                        d="M 0 3.214 C 0 1.004 1.843 0 3.214 0 C 4.586 0 6.429 0.603 6.429 3.214 C 6.429 5.826 3.214 5.913 3.214 7.232 C 3.214 8.552 3.214 8.571 3.214 8.571"
                        fill="transparent"
                        stroke-width="3.22"
                        stroke="#8A58FF"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    ></path>
                </g>
            </svg>
        </div>
    )
}

Icon.defaultProps = {
    width: 48,
    height: 48,
    iconSelection: "Framer",
    iconSearch: "Framer",
    color: "#888",
    selection: true,
}

// @ts-ignore
addPropertyControls(Icon, {
    color: { type: ControlType.Color, title: "Color" },
    selection: {
        type: ControlType.Boolean,
        title: "Find icon",
        enabledTitle: "Choose",
        disabledTitle: "Search",
    },
    iconSelection: {
        type: ControlType.Enum,
        options: Object.keys(FeatherIcons),
        defaultValue: Icon.defaultProps.iconSelection,
        title: indentTitle("Icon"),
        hidden: ({ selection }) => !selection,
    },
    iconSearch: {
        type: ControlType.String,
        title: indentTitle("Icon"),
        placeholder: "Menu, Wifi, Box…",
        hidden: ({ selection }) => selection,
    },
    ...defaultEvents,
})

const iconStyle: React.CSSProperties = {
    minWidth: "10px",
    minHeight: "10px",
    maxWidth: "20px",
    maxHeight: "20px",
    width: "60%",
    height: "60%",
}
