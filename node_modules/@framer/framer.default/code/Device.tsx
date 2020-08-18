import * as React from "react"
import {
    useCallback,
    useEffect,
    useLayoutEffect,
    useRef,
    useContext,
} from "react"
import {
    Color,
    Frame,
    Navigation,
    RenderTarget,
    motion,
    MotionPlugins,
    MotionPluginContext,
    addPropertyControls,
    ControlDescription,
    ControlType,
} from "framer"
import { colorFromToken } from "./lib/colorFromToken"

/*
 ** DEVICE
 */

interface DeviceDescriptor {
    title: string

    screenWidth: number
    screenHeight: number
    screenRadius?: number
    screenMask?: string

    bezelWidth?: number
    bezelHeight?: number
    bezelRadius?: number
}

function makeMaskImage({
    screenMask,
    screenWidth,
    screenHeight,
    landscape = false,
}: {
    screenMask: string
    screenWidth: number
    screenHeight: number
    landscape?: boolean
}) {
    const transform = landscape
        ? // rotate by 90 degreees counter-clockwise around (0,0), then move the
          // result down into the viewport (rightmost transform is applied first)
          `transform="translate(0 ${screenHeight}) rotate(-90)"`
        : ""
    const encoded = encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" viewport="0 0 ${screenWidth} ${screenHeight}" preserveAspectRatio="none"><g x="0" y="0" ${transform}>${screenMask}</g></svg>`
    )
    return `url("data:image/svg+xml;utf8,${encoded}")`
}

const preset_iPhonePro = {
    screenRadius: 38,
    bezelWidth: 21,
    bezelHeight: 21,
    bezelRadius: 38 + 21,
}
const preset_iPhone8 = {
    bezelWidth: 24,
    bezelHeight: 96,
    bezelRadius: 38 * 1.5,
}
const preset_iPadPro = {
    screenRadius: 25,
    bezelWidth: 38,
    bezelHeight: 38,
    bezelRadius: 25 + 38,
}
const preset_desktop = {
    bezelWidth: 20,
    bezelHeight: 20,
    bezelRadius: 20,
}

const defaultPreset = "iphone-11-pro"
const presets: { [key: string]: DeviceDescriptor } = {
    "iphone-11-pro": {
        title: "iPhone 11 Pro",
        ...preset_iPhonePro,
        screenWidth: 375,
        screenHeight: 812,
        screenMask:
            '<path d="M292 8.668V9c0 9.266-7.07 21-23.332 21h-162C90.402 30 83.332 18.266 83.332 9v-.332c0-4.285 0-8.668-7.664-8.668H43.332C16.312 0 0 16.313 0 43.332v725.336C0 795.688 16.313 812 43.332 812h288.336c27.02 0 43.332-16.313 43.332-43.332V43.332C375 16.312 358.687 0 331.668 0h-32C292 0 292 4.383 292 8.668zm0 0"/>',
    },
    "iphone-11-pro-max": {
        title: "iPhone 11 Pro Max",
        ...preset_iPhonePro,
        screenWidth: 414,
        screenHeight: 896,
        screenMask:
            '<path d="M96 0c3.313 0 5.91 2.688 6 6 .18 6.645 1.191 10.148 2.938 13.41 1.917 3.586 4.73 6.402 8.316 8.317 3.586 1.918 7.441 2.941 15.445 2.941h156.602c8.004 0 11.86-1.023 15.445-2.941 3.586-1.915 6.399-4.73 8.317-8.317 1.746-3.265 2.746-6.758 2.937-13.41.094-3.313 2.688-6 6-6h46.004c17.387 0 23.687 1.809 30.043 5.21 6.355 3.4 11.344 8.388 14.742 14.743C412.191 26.31 414 32.61 414 49.996v796.008c0 17.387-1.809 23.687-5.21 30.043-3.4 6.355-8.388 11.344-14.743 14.742-6.356 3.402-12.656 5.211-30.043 5.211H49.996c-17.387 0-23.687-1.809-30.043-5.21-6.355-3.4-11.344-8.388-14.742-14.743C1.809 869.69 0 863.39 0 846.004V49.996C0 32.61 1.809 26.31 5.21 19.953c3.4-6.355 8.388-11.344 14.743-14.742C26.31 1.809 32.61 0 49.996 0zm0 0"/>',
    },
    "iphone-8": {
        title: "iPhone 8",
        ...preset_iPhone8,
        screenWidth: 375,
        screenHeight: 667,
    },
    "iphone-8-plus": {
        title: "iPhone 8 Plus",
        ...preset_iPhone8,
        screenWidth: 414,
        screenHeight: 736,
    },
    "iphone-se": {
        title: "iPhone SE",
        screenWidth: 320,
        screenHeight: 568,
        bezelWidth: 20,
        bezelHeight: 112,
        bezelRadius: 38 * 1.5,
    },
    "samsung-note-10": {
        title: "Samsung Note 10",
        screenWidth: 360,
        screenHeight: 760,
        screenRadius: 10,
        bezelWidth: 7,
        bezelHeight: 15,
        bezelRadius: 15,
    },
    "pixel-4": {
        title: "Pixel 4",
        screenWidth: 360,
        screenHeight: 760,
        screenRadius: 30,
        bezelWidth: 10,
        bezelHeight: 40,
        bezelRadius: 50,
    },
    ipad: {
        title: "iPad",
        screenWidth: 768,
        screenHeight: 1024,
        bezelWidth: 30,
        bezelHeight: 95,
        bezelRadius: 38 * 1.5,
    },
    "ipad-pro-11": {
        title: "iPad Pro 11″",
        ...preset_iPadPro,
        screenWidth: 834,
        screenHeight: 1194,
    },
    "ipad-pro-12-9": {
        title: "iPad Pro 12.9″",
        ...preset_iPadPro,
        screenWidth: 1024,
        screenHeight: 1366,
    },
    "720p": {
        title: "720p",
        ...preset_desktop,
        screenWidth: 720,
        screenHeight: 1280,
    },
    "768p": {
        title: "768p",
        ...preset_desktop,
        screenWidth: 768,
        screenHeight: 1366,
    },
    "1080p": {
        title: "1080p",
        ...preset_desktop,
        screenWidth: 1080,
        screenHeight: 1920,
    },
    "1440p": {
        title: "1440p",
        ...preset_desktop,
        screenWidth: 1440,
        screenHeight: 2560,
    },
    "4k": {
        title: "4K",
        ...preset_desktop,
        screenWidth: 2160,
        screenHeight: 3840,
    },
}

interface Props {
    width: number
    height: number
    children?: React.ReactElement

    preset: string

    customScreenWidth: number
    customScreenHeight: number
    customScreenRadius: number
    customBezelWidth: number
    customBezelHeight: number
    customBezelRadius: number

    orientation: "portrait" | "landscape"

    backgroundColor: string
    backgroundImage?: string
    theme: "light" | "dark"
    shadow: boolean
}

export function Device({
    width,
    height,
    children,

    preset: presetName,

    customScreenWidth,
    customScreenHeight,
    customScreenRadius,
    customBezelWidth,
    customBezelHeight,
    customBezelRadius,

    orientation,

    backgroundColor: backgroundColorString,
    backgroundImage,
    theme,
    shadow,
}: Props) {
    //
    // size

    const padding = 50

    let {
        screenWidth,
        screenHeight,
        screenRadius = 0,
        screenMask = undefined,
        bezelWidth = 0,
        bezelHeight = 0,
        bezelRadius = 0,
    } =
        presetName === "custom"
            ? {
                  screenWidth: customScreenWidth,
                  screenHeight: customScreenHeight,
                  screenRadius: customScreenRadius,
                  bezelWidth: customBezelWidth,
                  bezelHeight: customBezelHeight,
                  bezelRadius: customBezelRadius,
              }
            : presets[presetName] || presets[Object.keys(presets)[0]]

    if (orientation === "landscape") {
        ;[screenWidth, screenHeight] = [screenHeight, screenWidth]
        ;[bezelWidth, bezelHeight] = [bezelHeight, bezelWidth]
    }

    const deviceWidth = screenWidth + 2 * bezelWidth
    const deviceHeight = screenHeight + 2 * bezelHeight

    const maskImage =
        screenMask &&
        makeMaskImage({
            screenMask,
            screenWidth,
            screenHeight,
            landscape: orientation === "landscape",
        })

    //
    // style

    const darkMode = theme === "dark"

    const backgroundColor = Color(colorFromToken(backgroundColorString))
    const screenColor = Color.alpha(backgroundColor, 0.1)

    const bezelColor = darkMode ? "#222" : "#fff"
    const bezelShade = `inset 0 0 15px ${
        darkMode
            ? "#000"
            : Color.toRgbString(Color.alpha(backgroundColor, 0.75))
    }`

    const deviceShadowColor = darkMode
        ? "rgba(0, 0, 0, 0.55)"
        : "rgba(0, 0, 0, 0.15)"
    const deviceShadow = `0px 10px 30px ${deviceShadowColor}`

    let deviceBoxShadow = bezelShade
    if (shadow) {
        deviceBoxShadow += `, ${deviceShadow}`
    }

    //
    // children

    const child = children[0]
    const resizedChild = child
        ? React.cloneElement(child, {
              width: screenWidth,
              height: screenHeight,
          })
        : null

    //
    // scaling

    const containerRef = useRef<HTMLDivElement>()
    const deviceRef = useRef<HTMLDivElement>()

    const scaleRef = useRef<number>()

    const computeScale = useCallback(
        ({ containerWidth, containerHeight }) => {
            const scaleX = (containerWidth - 2 * padding) / deviceWidth
            const scaleY = (containerHeight - 2 * padding) / deviceHeight
            const scale = Math.min(scaleX, scaleY, 1)
            return scale
        },
        [deviceWidth, deviceHeight, padding]
    )

    // in responsive preview, we can't rely on props to know our width and
    // height, so let's switch to measuring the actual size of the container
    const useContainerBasedScale =
        RenderTarget.current() === RenderTarget.preview

    // if using the prop-based scale, update scaleRef on each render
    if (!useContainerBasedScale) {
        scaleRef.current = computeScale({
            containerWidth: width,
            containerHeight: height,
        })
    }

    const applyContainerBasedScale = useCallback(() => {
        const container = containerRef.current
        const device = deviceRef.current
        if (!container || !device) return

        scaleRef.current = computeScale({
            containerWidth: container.offsetWidth,
            containerHeight: container.offsetHeight,
        })
        device.style.transform = `scale(${scaleRef.current})`
    }, [containerRef, deviceRef, scaleRef])

    useEffect(() => {
        if (useContainerBasedScale) {
            // apply on mount
            applyContainerBasedScale()

            window.addEventListener("resize", applyContainerBasedScale)
        }
        return () =>
            window.removeEventListener("resize", applyContainerBasedScale)
    }, [useContainerBasedScale, applyContainerBasedScale])

    // ensure Motion gestures still work correctly despite the scale
    const { transformPagePoint: originalTransformPagePoint } = useContext(
        MotionPluginContext
    )
    const transformPagePoint = useCallback(
        ({ x, y }) =>
            originalTransformPagePoint({
                x: x / scaleRef.current,
                y: y / scaleRef.current,
            }),
        [scaleRef]
    )

    //
    // render

    return (
        <div
            ref={containerRef}
            style={{
                width: "100%",
                height: "100%",
                flexShrink: 0,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                overflow: "hidden",
                backgroundColor: backgroundColorString,
                backgroundImage:
                    backgroundImage &&
                    `url(${decodeURIComponent(backgroundImage)})`,
                backgroundPosition: "center",
                backgroundSize: "cover",
            }}
        >
            <div
                ref={deviceRef}
                style={{
                    width: deviceWidth,
                    height: deviceHeight,
                    flexShrink: 0,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    overflow: "hidden",
                    borderRadius: bezelRadius,
                    backgroundColor: bezelColor,
                    boxShadow: deviceBoxShadow,
                    transform: scaleRef.current && `scale(${scaleRef.current})`,
                }}
            >
                <div
                    style={{
                        width: screenWidth,
                        height: screenHeight,
                        flexShrink: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        overflow: "hidden",
                        borderRadius: screenRadius,
                        backgroundColor: Color.toRgbString(screenColor),
                        ...(screenMask && {
                            maskImage,
                            WebkitMaskImage: maskImage,
                            maskSize: "contain",
                            WebkitMaskSize: "contain",
                        }),
                    }}
                >
                    <MotionPlugins transformPagePoint={transformPagePoint}>
                        {resizedChild ? (
                            <Navigation>{resizedChild}</Navigation>
                        ) : null}
                    </MotionPlugins>
                </div>
            </div>

            {!resizedChild && RenderTarget.current() === RenderTarget.canvas && (
                <div
                    style={{
                        position: "absolute",
                        right: 20,
                        top: "50%",
                        fontSize: "50pt",
                        height: "200px",
                        lineHeight: "200px",
                        marginTop: "-102px",
                        color: "#fff",
                        textShadow: "0px 5px 10px rgba(0, 0, 0, 0.15)",
                    }}
                >
                    →
                </div>
            )}
        </div>
    )
}

const defaultProps: Props = {
    width: 1920,
    height: 1080,

    preset: defaultPreset,

    customScreenWidth: 200,
    customScreenHeight: 400,
    customScreenRadius: 0,
    customBezelWidth: 20,
    customBezelHeight: 20,
    customBezelRadius: 20,

    orientation: "portrait",

    backgroundColor: "#09f",
    theme: "light",
    shadow: true,
}
Device.defaultProps = defaultProps

function customDeviceConfig(
    title: string,
    min: number,
    max: number
): ControlDescription<Partial<Props>> {
    return {
        type: ControlType.Number,
        title,
        min,
        max,
        displayStepper: true,
        hidden: (props) => props.preset !== "custom",
    }
}

addPropertyControls(Device, {
    preset: {
        type: ControlType.Enum,
        options: [...Object.keys(presets), "custom"],
        optionTitles: [
            ...Object.keys(presets).map((p) => presets[p].title),
            "Custom",
        ],
    },

    customScreenWidth: customDeviceConfig("Screen Width", 10, 10000),
    customScreenHeight: customDeviceConfig("Screen Height", 10, 10000),
    customScreenRadius: customDeviceConfig("Screen Radius", 0, 10000),
    customBezelWidth: customDeviceConfig("Bezel Width", 0, 10000),
    customBezelHeight: customDeviceConfig("Bezel Height", 0, 10000),
    customBezelRadius: customDeviceConfig("Bezel Radius", 0, 10000),

    orientation: {
        type: ControlType.Enum,
        displaySegmentedControl: true,
        options: ["portrait", "landscape"],
        optionTitles: ["Portrait", "Landscape"],
    },

    backgroundColor: { type: ControlType.Color, title: "Background" },
    backgroundImage: {
        type: ControlType.File,
        allowedFileTypes: ["jpg", "jpeg", "png"],
        title: "Bg Image",
    },
    theme: {
        type: ControlType.Enum,
        displaySegmentedControl: true,
        options: ["light", "dark"],
        optionTitles: ["Light", "Dark"],
    },
    shadow: {
        type: ControlType.Boolean,
        enabledTitle: "On",
        disabledTitle: "Off",
    },
})
