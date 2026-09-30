init python:
    def change_energy(amount):
        global energy, energy_feedback, energy_feedback_serial
        previous = energy
        energy = max(0, min(100, energy + amount))
        energy_feedback = energy - previous
        energy_feedback_serial += 1
        return energy

