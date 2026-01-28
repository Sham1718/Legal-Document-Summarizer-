package com.legalai.backend.service;

import com.legalai.backend.dto.AskRequest;
import com.legalai.backend.dto.AskResponse;
import com.legalai.backend.dto.QueryHistoryDto;
import com.legalai.backend.entity.QueryHistory;

import com.legalai.backend.entity.User;
import com.legalai.backend.repository.QueryHistroyRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

@Service
public class RagClientService {

    private final WebClient webClient;
    private final QueryHistroyRepository queryHistroyRepository;

    public RagClientService(WebClient webClient,  QueryHistroyRepository queryHistroyRepository) {
        this.webClient = webClient;
        this.queryHistroyRepository = queryHistroyRepository;

    }

    public AskResponse askQuestion(String question, User user) {

        AskResponse response = webClient.post()
                .uri("/ask")
                .bodyValue(new AskRequest(question))
                .retrieve()
                .bodyToMono(AskResponse.class)
                .timeout(Duration.ofSeconds(5))
                .onErrorReturn(new AskResponse(
                        "Answer service temporarily unavailable.",
                        List.of()
                ))
                .block();

        // ---- Persist query ----
        QueryHistory history = new QueryHistory();
        history.setQuestion(question);
        history.setAnswer(response.getAnswer());
        history.setUser(user);

        if (response.getSources() != null) {
            history.setSources(
                    String.join(",",response.getSources())
            );
        }
        queryHistroyRepository.save(history);
        return response;
    }



    public Page<QueryHistoryDto> getHistory(User user, PageRequest pageRequest) {

        Page<QueryHistory> history =
                queryHistroyRepository.findByUserOrderByCreatedAtDesc(
                        user, pageRequest
                );

        return history.map(h -> new QueryHistoryDto(
                h.getQuestion(),
                h.getAnswer(),
                h.getSources(),
                h.getCreatedAt()
        ));
    }
}
