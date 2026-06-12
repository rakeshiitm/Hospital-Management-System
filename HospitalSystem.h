#ifndef HOSPITALSYSTEM_H
#define HOSPITALSYSTEM_H

#include <unordered_map>
#include <queue>
#include <vector>
#include <string>
#include "Patient.h"

class HospitalSystem {
private:
    std::unordered_map<int, Patient> records;
    std::priority_queue<Patient, std::vector<Patient>, Patient::PriorityComparator> opdQueue;
    int nextPatientId;
    const std::string dataFile = "patients.txt";

public:
    HospitalSystem();
    ~HospitalSystem();

    void addPatient(std::string name, int age, std::string disease, int priority);
    void searchPatient(int id) const;
    void dischargePatient(int id);
    void serveNextPatient();
    void displayAll() const;

    void saveData() const;
    void loadData();
};

#endif // HOSPITALSYSTEM_H
