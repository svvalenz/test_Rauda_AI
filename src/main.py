from evaluator import TicketEvaluator
import os

def main():
    evaluator = TicketEvaluator('docs/tickets (1).csv')
    results = evaluator.process_all_tickets()
    print(f"Evaluación completada. Resultados guardados en 'tickets_evaluated.csv'")
    print("\nPrimeras evaluaciones:")
    print(results.head())

if __name__ == "__main__":
    main() 