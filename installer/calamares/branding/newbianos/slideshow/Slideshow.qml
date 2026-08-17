import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    width: 600
    height: 400

    property int currentSlide: 0
    property var slides: [
        {
            title: "Antigravity-IDE Out-of-the-Box",
            desc: "AI-native development environment pre-configured with Node.js 22, Python 3.13, Docker, Git, and Wayland Ozone acceleration.",
            tag: "AI DEVELOPMENT"
        },
        {
            title: "Jarvis Multimodal Assistant",
            desc: "On-device voice and optical vision daemon, holographic HUD, and deep OS authority across hardware, containers, and packages.",
            tag: "MULTIMODAL AI"
        },
        {
            title: "Google Drive Workspace & Chrome",
            desc: "Bidirectional cloud sync mounted directly at ~/GoogleDrive in Dolphin Files, plus official Chrome with Widevine DRM and VA-API decode.",
            tag: "CLOUD & PRODUCTIVITY"
        },
        {
            title: "Figma Desktop & Developer Toolchain",
            desc: "Figma desktop with local font daemon, KDE Plasma 6 Wayland, Starship prompt, and cutting-edge Linux Kernel 7.x+ with PREEMPT_DYNAMIC scheduling.",
            tag: "DESIGN & SPEED"
        }
    ]

    Timer {
        interval: 8000
        running: true
        repeat: true
        onTriggered: {
            root.currentSlide = (root.currentSlide + 1) % root.slides.length
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "#030814"

        ColumnLayout {
            anchors.centerIn: parent
            width: parent.width - 60
            spacing: 16

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 140
                height: 28
                radius: 14
                color: "#00f0ff"
                opacity: 0.2
                border.color: "#00f0ff"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: root.slides[root.currentSlide].tag
                    color: "#00f0ff"
                    font.pixelSize: 11
                    font.bold: true
                    font.family: "JetBrains Mono"
                }
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: root.slides[root.currentSlide].title
                color: "#ffffff"
                font.pixelSize: 22
                font.bold: true
                font.family: "Orbitron"
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                text: root.slides[root.currentSlide].desc
                color: "#94a3b8"
                font.pixelSize: 13
                wrapMode: Text.WordWrap
                font.family: "JetBrains Mono"
            }
        }
    }
}
