#include "HospitalSystem.h"
#include <iostream>
#include <limits>

void clearInput() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

int main() {
    HospitalSystem system;
    int choice;

    std::cout << "--- Welcome to the Hospital Management System ---" << std::endl;

    while (true) {
        std::cout << "\n1. Add Patient\n2. Search Patient\n3. Discharge Patient\n4. Serve Next Patient (OPD)\n5. Display All Records\n6. Exit\nChoice: ";
        
        if (!(std::cin >> choice)) {
            std::cout << "Invalid input. Please enter a number." << std::endl;
            clearInput();
            continue;
        }

        switch (choice) {
            case 1: {
                std::string name, disease;
                int age, priority;
                std::cout << "Enter Name: ";
                clearInput();
                std::getline(std::cin, name);
                std::cout << "Enter Age: ";
                std::cin >> age;
                std::cout << "Enter Disease: ";
                clearInput();
                std::getline(std::cin, disease);
                std::cout << "Enter Priority (1: Critical, 5: Normal): ";
                std::cin >> priority;
                system.addPatient(name, age, disease, priority);
                break;
            }
            case 2: {
                int id;
                std::cout << "Enter Patient ID: ";
                std::cin >> id;
                system.searchPatient(id);
                break;
            }
            case 3: {
                int id;
                std::cout << "Enter Patient ID to discharge: ";
                std::cin >> id;
                system.dischargePatient(id);
                break;
            }
            case 4:
                system.serveNextPatient();
                break;
            case 5:
                system.displayAll();
                break;
            case 6:
                std::cout << "Exiting system. Data saved." << std::endl;
                return 0;
            default:
                std::cout << "Invalid choice. Try again." << std::endl;
        }
    }

    return 0;
}
