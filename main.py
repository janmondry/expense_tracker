import Model
import controller
import GUI
import logowanieGUI

# przykładowe dane do logowania:
# login: login1
# hasło: haslo1

def main():
    ctrl = controller.Controller()
    ctrl.addModel(Model.Database())
    ctrl.addView(logowanieGUI.LogowanieGUI(ctrl))
    ctrl.showLoggingGUI()


if __name__ == "__main__":
    main()
