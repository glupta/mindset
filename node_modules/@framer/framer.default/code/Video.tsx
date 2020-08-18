import * as React from "react"
import { Frame, PropertyControls, ControlType, RenderTarget } from "framer"
import { cachedResponse, corsProxy, hashCode } from "./lib/Cache"
import { defaultEvents } from "./lib/constants"

/*
 ** VIDEO
 */

type VideoProps = {
    srcType: SrcType
    srcUrl: string
    srcFile: string
    poster: string
    autoPlay: boolean
    canvasPlay: boolean
    controls: boolean
    muted: boolean
    loop: boolean
    playsinline: boolean
    preload: PreloadType
    objectFit: ObjectFitType
    backgroundColor: string
    radius: number
    onEnd?: Function
    onSeeked?: Function
    onPause?: Function
    onPlay?: Function
    topLeft?: number
    topRight?: number
    bottomRight?: number
    bottomLeft?: number
    isMixed?: boolean
    onClick?: any
    onMouseEnter?: any
    onMouseLeave?: any
    onMouseDown?: any
    onMouseUp?: any
}

enum ObjectFitType {
    Fill = "fill",
    Contain = "contain",
    Cover = "cover",
    None = "none",
    ScaleDown = "scale-down",
}

enum PreloadType {
    None = "none",
    MetaData = "metadata",
    Auto = "auto",
    ForceCache = "force",
}

enum SrcType {
    Video = "Upload",
    Url = "URL",
}

export class Video extends React.Component<VideoProps> {
    static defaultProps: VideoProps = {
        srcType: SrcType.Url,
        srcUrl: "https://assets.mixkit.co/videos/1076/1076-720.mp4",
        srcFile: "",
        poster:
            "https://mixkit.imgix.net/videos/preview/mixkit-surfer-riding-the-waves-1076-0.jpg",
        controls: false,
        autoPlay: true,
        canvasPlay: false,
        loop: true,
        muted: false,
        playsinline: true,
        preload: PreloadType.Auto,
        objectFit: ObjectFitType.Cover,
        backgroundColor: "rgba(0,0,0,0)",
        radius: 0,
    }

    static propertyControls: PropertyControls<VideoProps> = {
        srcType: {
            type: ControlType.SegmentedEnum,
            title: "Source",
            options: [SrcType.Url, SrcType.Video],
        },
        srcUrl: {
            type: ControlType.String,
            title: " ",
            placeholder: ".../example.mp4",
            hidden(props) {
                return props.srcType === SrcType.Video
            },
        },

        srcFile: {
            type: ControlType.File,
            title: " ",
            allowedFileTypes: ["mp4"],
            hidden(props) {
                return props.srcType === SrcType.Url
            },
        },
        poster: { type: ControlType.Image },
        backgroundColor: {
            type: ControlType.Color,
            title: "Background",
        },
        radius: {
            title: "Radius",
            type: ControlType.FusedNumber,
            toggleKey: "isMixed",
            toggleTitles: ["Radius", "Radius per corner"],
            valueKeys: ["topLeft", "topRight", "bottomRight", "bottomLeft"],
            valueLabels: ["TL", "TR", "BR", "BL"],
            min: 0,
        },
        objectFit: {
            type: ControlType.Enum,
            title: "Fit",
            options: [
                ObjectFitType.Cover,
                ObjectFitType.Fill,
                ObjectFitType.Contain,
                ObjectFitType.ScaleDown,
                ObjectFitType.None,
            ],
        },

        autoPlay: {
            type: ControlType.Boolean,
            title: "Auto Play",
            enabledTitle: "Yes",
            disabledTitle: "No",
        },
        loop: {
            type: ControlType.Boolean,
            title: "Loop",
            enabledTitle: "Yes",
            disabledTitle: "No",
        },
        controls: {
            type: ControlType.Boolean,
            title: "Controls",
            enabledTitle: "Show",
            disabledTitle: "Hide",
        },

        muted: {
            type: ControlType.Boolean,
            title: "Muted",
            enabledTitle: "Yes",
            disabledTitle: "No",
        },
        // playsinline: { type: ControlType.Boolean, title: "Inline", enabledTitle: "Yes", disabledTitle: "No" },
        canvasPlay: {
            type: ControlType.Boolean,
            title: "On Canvas",
            enabledTitle: "Play",
            disabledTitle: "Pause",
            hidden(props) {
                return props.autoPlay === false
            },
        },
        preload: {
            type: ControlType.Enum,
            title: "Preload",
            options: [
                PreloadType.Auto,
                PreloadType.MetaData,
                PreloadType.None,
                PreloadType.ForceCache,
            ],
        },
        onEnd: { type: ControlType.EventHandler },
        onSeeked: { type: ControlType.EventHandler },
        onPause: { type: ControlType.EventHandler },
        onPlay: { type: ControlType.EventHandler },
        ...defaultEvents,
    }

    videoRef: React.Ref<HTMLVideoElement> = null

    setVideoRef = async (element) => {
        this.videoRef = element

        const { srcUrl, preload, srcType } = this.props

        if (preload === PreloadType.ForceCache) {
            const url = this.url(true)
            const response = await cachedResponse(url)
            if (response && this.videoRef) {
                this.videoRef["src"] = URL.createObjectURL(response) // IE10+
            }
        }
    }

    url(cors = false) {
        if (this.props.srcType === SrcType.Url) {
            return cors ? corsProxy(this.props.srcUrl) : this.props.srcUrl
        }

        if (this.props.srcType === SrcType.Video) {
            return this.props.srcFile
        }
    }

    render() {
        const {
            srcType,
            srcFile,
            srcUrl,
            autoPlay,
            canvasPlay,
            loop,
            muted,
            playsinline,
            controls,
            preload,
            objectFit,
            backgroundColor,
            radius,
            topLeft,
            topRight,
            bottomRight,
            bottomLeft,
            isMixed,
            onSeeked,
            onPause,
            onPlay,
            onEnd,
            onClick,
            onMouseEnter,
            onMouseLeave,
            onMouseDown,
            onMouseUp,
            poster,
        } = this.props
        const isCanvas = RenderTarget.current() != RenderTarget.preview
        const isForcedCache = preload === PreloadType.ForceCache
        const key = hashCode(
            JSON.stringify({
                srcType,
                srcUrl,
                srcFile,
                autoPlay,
                canvasPlay,
                isForcedCache,
            })
        )

        const borderRadius = isMixed
            ? `${topLeft}px ${topRight}px ${bottomRight}px ${bottomLeft}px`
            : `${radius}px`

        return (
            <div
                {...{
                    onClick,
                    onMouseEnter,
                    onMouseLeave,
                    onMouseDown,
                    onMouseUp,
                }}
                style={{
                    width: "100%",
                    height: "100%",
                    overflow: "hidden",
                    backgroundColor: backgroundColor,
                    borderRadius,
                    WebkitMaskImage: "-webkit-radial-gradient(white, black)",
                }}
            >
                <video
                    ref={isForcedCache ? this.setVideoRef : null}
                    key={key}
                    poster={poster}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: objectFit,
                        objectPosition: "50% 50%",
                    }}
                    onSeeked={(e) => {
                        if (onSeeked) onSeeked(e)
                    }}
                    onPause={(e) => {
                        if (onPause) onPause(e)
                    }}
                    onPlay={(e) => {
                        if (onPlay) onPlay(e)
                    }}
                    onEnded={(e) => {
                        if (onEnd) onEnd(e)
                    }}
                    src={isForcedCache ? null : this.url()}
                    autoPlay={isCanvas ? canvasPlay : autoPlay}
                    controls={isCanvas ? false : controls}
                    muted={isCanvas ? true : muted}
                    loop={loop}
                    playsInline={playsinline}
                    preload={preload}
                />
            </div>
        )
    }
}
