package lab.aui.model_service.domain.command;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CreateModelCommand {
    private String name;
    private int year;
    private double engine;
}