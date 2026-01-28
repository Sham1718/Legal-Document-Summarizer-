package com.legalai.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@AllArgsConstructor
public class QueryHistoryDto {
    private String question;
    private String answer;
    private String createdAt;
    private LocalDateTime sources;
}
