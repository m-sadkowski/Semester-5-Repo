package lab.aui.app.domain.command;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
public class CreateModelCommand {
    private final UUID id;
    private final String name;
    private final int year;
    private final double engine;
    private final UUID brandId;
}
