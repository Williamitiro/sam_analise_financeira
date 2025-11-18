// frontend/src/lib/api/mockCohortData.ts

// Generates a mock cohort matrix
// Each row is a cohort (e.g., users who signed up in Month 1)
// Each column is the retention in the months following signup
export const generateMockCohortData = (months = 12) => {
    const data = [];
    for (let i = 0; i < months; i++) {
        const cohortSize = 100 + i * 10; // Growing cohort size
        const row = {
            cohort: `Mês ${i + 1}`,
            size: cohortSize,
            retention: [] as (number | null)[],
        };
        let retention = 100;
        for (let j = 0; j < months; j++) {
            if (j < i) {
                row.retention.push(null); // No data for future months relative to cohort
            } else {
                row.retention.push(Math.round(retention));
                retention *= (0.95 - i * 0.005); // Each cohort has slightly worse retention
                if (retention < 20) retention = 20;
            }
        }
        data.push(row);
    }
    return data;
};

export const MOCK_COHORT_DATA = generateMockCohortData(12);
