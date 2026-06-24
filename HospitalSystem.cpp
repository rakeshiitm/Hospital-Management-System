#include "HospitalSystem.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
using namespace std;
HospitalSystem::HospitalSystem() : nextPatientId(1) {
    loadData();
}

HospitalSystem::~HospitalSystem() {
    saveData();
}

void HospitalSystem::addPatient(string name, int age, string disease, int priority) {
    Patient p = {nextPatientId++, name, age, disease, priority};
    records[p.id] = p;
    opdQueue.push(p);
    cout << "Patient added successfully. ID: " << p.id <<endl;
}

void HospitalSystem::searchPatient(int id) const {
    auto it = records.find(id);
    if (it != records.end()) {
        const Patient& p = it->second;
        cout << "\n--- Patient Record Found ---" << endl;
        cout << "ID: " << p.id << "\nName: " << p.name << "\nAge: " << p.age 
                  << "\nDisease: " << p.disease << "\nPriority: " << p.priorityLevel << endl;
    } else {
        cout << "Patient with ID " << id << " not found." << endl;
    }
}

void HospitalSystem::dischargePatient(int id) {
    if (records.erase(id)) {
        cout << "Patient with ID " << id << " has been discharged." << endl;
    } else {
        cout << "Patient with ID " << id << " not found." << endl;
    }
}

void HospitalSystem::serveNextPatient() {
    while (!opdQueue.empty()) {
        Patient p = opdQueue.top();
        opdQueue.pop();
        if (records.find(p.id) != records.end()) {
            cout << "--- Serving Patient ---" << endl;
            cout << "ID: " << p.id << "\nName: " << p.name << "\nPriority: " << p.priorityLevel << endl;
            records.erase(p.id); 
            return;
        }
    }
    cout << "No patients in the OPD queue." << endl;
}

void HospitalSystem::displayAll() const {
    if (records.empty()) {
        cout << "No patient records available." << endl;
        return;
    }

    cout << "\n" << left << setw(5) << "ID" << setw(20) << "Name" 
              << setw(5) << "Age" << setw(20) << "Disease" << "Priority" << endl;
    cout << string(60, '-') << endl;

    for (auto const& [id, p] : records) {
        cout << left << setw(5) << p.id << setw(20) << p.name 
                  << setw(5) << p.age << setw(20) << p.disease << p.priorityLevel << endl;
    }
}

void HospitalSystem::saveData() const {
    ofstream outFile(dataFile);
    if (!outFile) {
        cerr << "Error: Could not open file for saving." << endl;
        return;
    }

    outFile << nextPatientId << "\n";
    for (auto const& [id, p] : records) {
        outFile << p.id << "|" << p.name << "|" << p.age << "|" << p.disease << "|" << p.priorityLevel << "\n";
    }
    outFile.close();
}

void HospitalSystem::loadData() {
    ifstream inFile(dataFile);
    if (!inFile) return;

    string line;
    if (getline(inFile, line)) {
        nextPatientId = stoi(line);
    }

    while (getline(inFile, line)) {
        stringstream ss(line);
        string segment;
        vector<string> data;

        while (getline(ss, segment, '|')) {
            data.push_back(segment);
        }

        if (data.size() == 5) {
            Patient p;
            p.id = stoi(data[0]);
            p.name = data[1];
            p.age = stoi(data[2]);
            p.disease = data[3];
            p.priorityLevel = stoi(data[4]);

            records[p.id] = p;
            opdQueue.push(p);
        }
    }
    inFile.close();
}
