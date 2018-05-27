# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:40:18 2018

@author: Adrian
"""

alphabet = set(['A', 'C', 'T', 'G'])
diag_score = 10
off_diag_score = 4
dash_score = -6

seq_x = 'AA' 
seq_y = 'TAAT'

scoring_matrix = build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False)

