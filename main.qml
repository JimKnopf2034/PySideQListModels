import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15



Window {
    id: window
    visible: true
    height: 200
    width: 400

    Rectangle {
        id: mainArea
        anchors.fill: parent
        ColumnLayout {
            anchors.fill: parent
            
            ComboBox {
                id: cBox
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                model: stringModel
                textRole: "display"
            }
            RowLayout{
                    Layout.alignment: Qt.AlignHCenter
                Button {
                    id: addOne
                    text: qsTr("Add One")
                    onClicked: bridge.add_one()
                }
                Button {
                    id: quit
                    text: qsTr("Quit")
                    onClicked : window.close()
                }
            }
        }

    }
}