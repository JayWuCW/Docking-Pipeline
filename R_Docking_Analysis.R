df <- read_csv("docking_results.csv")

df |>
+     arrange(best_affinity_kcal_mol)

df |>
+     arrange(best_affinity_kcal_mol) |>
+     mutate(rank = row_number()) |>
+     filter(label == "control") |>
+     select(ligand_id, best_affinity_kcal_mol, rank)

 df |>
+     group_by(label) |>
+     summarise(
+         n          = n(),
+         mean_score = mean(best_affinity_kcal_mol),
+         best_score = min(best_affinity_kcal_mol)

> ggplot(df, aes(x = best_affinity_kcal_mol)) +
+     geom_histogram(bins = 15, fill = "blue", colour = "white") +
+     geom_vline(
+         data = filter(df, label == "control"),
+         aes(xintercept = best_affinity_kcal_mol),
+         colour = "red"
+     ) +
+     labs(x = "Binding affinity (kcal/mol)", y = "Number of drugs",
+          title = "Docking scores (red lines = known AChE drugs)") +
+     theme_minimal()
>
> ggsave("Docking_Score_Histogram.png", width = 7, height = 5)

> ggplot(df, aes(x = label, y = best_affinity_kcal_mol, fill = label)) +
+     geom_boxplot(alpha = 0.5) +
+     geom_jitter(width = 0.15) +
+     labs(x = NULL, y = "Binding affinity (kcal/mol)") +
+     theme_minimal() +
+     theme(legend.position = "none")
>
> ggsave("controls_vs_background.png", width = 6, height = 5)
