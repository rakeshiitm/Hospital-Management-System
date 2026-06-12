#include "HospitalSystem.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

HospitalSystem::HospitalSystem() : nextPatientId(1) {
    loadData();
}

HospitalSystem::~HospitalSystem() {
    saveData();
}

void HospitalSystem::addPatient(std::string name, int age, std::string disease, int priority) {
    Patient p = {nextPatientId++, name, age, disease, priority};
    records[p.id] = p;
    opdQueue.push(p);
    std::cout << "Patient added successfully. ID: " << p.id << std::endl;
}

void HospitalSystem::searchPatient(int id) const {
    auto it = records.find(id);
    if (it != records.end()) {
        const Patient& p = it->second;
        std::cout << "\n--- Patient Record Found ---" << std::endl;
        std::cout << "ID: " << p.id << "\nName: " << p.name << "\nAge: " << p.age 
                  << "\nDisease: " << p.disease << "\nPriority: " << p.priorityLevel << std::endl;
    } else {
        std::cout << "Patient with ID " << id << " not found." << std::endl;
    }
}

void HospitalSystem::dischargePatient(int id) {
    if (records.erase(id)) {
        std::cout << "Patient with ID " << id << " has been discharged." << std::endl;
        // Note: The patient remains in the priority queue but will be ignored when served
        // if not found in the records map.
    } else {
        std::cout << "Patient with ID " << id << " not found." << std::endl;
    }
}

void HospitalSystem::serveNextPatient() {
    while (!opdQueue.empty()) {
        Patient p = opdQueue.top();
        opdQueue.pop();

        // Check if the patient still exists (wasn't discharged)
        if (records.find(p.id) != records.end()) {
            std::cout << "\n--- Serving Patient ---" << std::endl;
            std::cout << "ID: " << p.id << "\nName: " << p.name << "\nPriority: " << p.priorityLevel << std::endl;
            records.erase(p.id); // Remove from records after serving
            return;
        }
    }
    std::cout << "No patients in the OPD queue." << std::endl;
}

void HospitalSystem::displayAll() const {
    if (records.empty()) {
        std::cout << "No patient records available." << std::endl;
        return;
    }

    std::cout << "\n" << std::left << std::setw(5) << "ID" << std::setw(20) << "Name" 
              << std::setw(5) << "Age" << std::setw(20) << "Disease" << "Priority" << std::endl;
    std::cout << std::string(60, '-') << std::endl;

    for (auto const& [id, p] : records) {
        std::cout << std::left << std::setw(5) << p.id << std::setw(20) << p.name 
                  << std::setw(5) << p.age << std::setw(20) << p.disease << p.priorityLevel << std::endl;
    }
}

void HospitalSystem::saveData() const {
    std::ofstream outFile(dataFile);
    if (!outFile) {
        std::cerr << "Error: Could not open file for saving." << std::endl;
        return;
    }

    outFile << nextPatientId << "\n";
    for (auto const& [id, p] : records) {
        outFile << p.id << "|" << p.name << "|" << p.age << "|" << p.disease << "|" << p.priorityLevel << "\n";
    }
    outFile.close();
}

void HospitalSystem::loadData() {
    std::ifstream inFile(dataFile);
    if (!inFile) return;

    std::string line;
    if (std::getline(inFile, line)) {
        nextPatientId = std::stoi(line);
    }

    while (std::getline(inFile, line)) {
        std::stringstream ss(line);
        std::string segment;
        std::vector<std::string> data;

        while (std::getline(ss, segment, '|')) {
            data.push_back(segment);
        }

        if (data.size() == 5) {
            Patient p;
            p.id = std::stoi(data[0]);
            p.name = data[1];
            p.age = std::stoi(data[2]);
            p.disease = data[3];
            p.priorityLevel = std::stoi(data[4]);

            records[p.id] = p;
            opdQueue.push(p);
        }
    }
    inFile.close();
}
